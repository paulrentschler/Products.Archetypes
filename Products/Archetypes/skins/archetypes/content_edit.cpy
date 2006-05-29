## Script (Python) "content_edit"
##title=Edit content
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=id=''

REQUEST = context.REQUEST

new_context = context.portal_factory.doCreate(context, id)
new_context.processForm()

portal_status_message = REQUEST.get('portal_status_message', 'Content changes saved.')

# handle navigation for multi-page edit forms
next = not REQUEST.get('form_next',None) is None
previous = not REQUEST.get('form_previous',None) is None
if next or previous:
    fieldset = REQUEST.get('fieldset', None)

    schematas = [s for s in new_context.Schemata().keys() if s != 'metadata']

    if previous:
        schematas.reverse()

    next_schemata = None
    try:
        index = schematas.index(fieldset)
    except ValueError:
        raise 'Non-existing fieldset: %s' % fieldset
    else:
        index += 1
        if index < len(schematas):
            next_schemata = schematas[index]
            return state.set(status='next_schemata', \
                             context=new_context, \
                             fieldset=next_schemata, \
                             portal_status_message=portal_status_message)

    if next_schemata == None:
        raise 'Unable to find next field set after %s' % fieldset

return state.set(status='success',\
                 context=new_context,\
                 portal_status_message=portal_status_message)
