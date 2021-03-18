# encoding: utf-8


from Acquisition import aq_parent, aq_inner
from Products.CMFCore.interfaces import IFolderish
from Products.CMFCore.WorkflowCore import WorkflowException
import transaction, logging, plone.api, StringIO

app = globals().get('app')  # ``zope run`` magic


def _convert(context, wfTool=None):
    if wfTool is None:
        wfTool = plone.api.portal.get_tool('portal_workflow')
    logging.info(u'😉 Converting items in %r', context)
    portal_type = context.portal_type
    if portal_type in ('IPDA File', 'IPDA Event'):
        status, parent = wfTool.getStatusOf('plone_workflow', context), aq_parent(context)
        objID, title, descr, owner = context.id, context.title, context.description, context.getOwner()
        if portal_type == 'IPDA File':
            dumbDocumentID = context.documentID if context.documentID else u'«unknown»'
            if context.getFile().getSize() > 0:
                contentType, data, fn = context.getFile().getContentType(), context.getFile().data, context.getFile().getFilename()
            else:
                data = None
        elif portal_type == 'IPDA Event':
            location, startDate, endDate = context.location, context.startDate, context.endDate
            text, attendees, eventUrl = context.getText(), context.attendees, context.eventUrl
            n, e, p = context.contactName, context.contactEmail, context.contactPhone
        parent.manage_delObjects([objID])
        logging.info(u'🆕 Creating %s', objID)
        o = None
        if portal_type == 'IPDA File' and data is not None:
            o = parent[parent.invokeFactory('File', objID)]
            o.setTitle(title)
            o.setDescription(descr + u'. Document ID = ' + dumbDocumentID)
            o.setFile(StringIO.StringIO(data), mimetype=contentType, filename=fn)
            o.changeOwnership(owner)
        elif portal_type == 'IPDA Event':
            o = parent[parent.invokeFactory('Event', objID)]
            o.setTitle(title)
            o.setDescription(descr)
            o.setLocation(location)
            o.setStartDate(startDate)
            o.setEndDate(endDate)
            o.setText(text)
            o.setAttendees(attendees)
            o.setEventUrl(eventUrl)
            o.setContactName(n)
            o.setContactEmail(e)
            o.setContactPhone(p)
            o.changeOwnership(owner)
        if o and status and status['review_state'] == 'published':
            try:
                wfTool.doActionFor(o, action='publish')
            except WorkflowException:
                pass
    if IFolderish.providedBy(context):
        for childID, childItem in context.contentItems():
            _convert(childItem, wfTool)


def _delete(context):
    if IFolderish.providedBy(context):
        for childID, childItem in context.contentItems():
            _delete(childItem)
    if context.portal_type in ('FormFolder', 'Steering Committee Display'):
        parent = aq_parent(context)
        logging.warn(u'💥 Deleting %r', context)
        parent.manage_delObjects([context.id])


def _convertZenderCrap(app):
    logging.warn(u'😲 OK HERE WE GO')
    portal = app['planetarydata']
    _convert(portal)
    _delete(portal)
    catalog = plone.api.portal.get_tool('portal_catalog')
    catalog.clearFindAndRebuild()
    transaction.commit()


def main():
    global app
    _convertZenderCrap(app)


if __name__ == '__main__':
    main()