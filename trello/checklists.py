import json
import requests

class Checklists(object):
    __module__ = 'trello'

    def __init__(self, apikey, token=None):
        self._apikey = apikey
        self._token = token

    def get(self, idChecklist, cards=None, card_fields=None, checkItems=None, checkItem_fields=None, fields=None):
        resp = requests.get("https://trello.com/1/checklists/%s" % (idChecklist), params=dict(key=self._apikey, token=self._token, cards=cards, card_fields=card_fields, checkItems=checkItems, checkItem_fields=checkItem_fields, fields=fields), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_field(self, field, idChecklist):
        resp = requests.get("https://trello.com/1/checklists/%s/%s" % (idChecklist, field), params=dict(key=self._apikey, token=self._token), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_board(self, idChecklist, fields=None):
        resp = requests.get("https://trello.com/1/checklists/%s/board" % (idChecklist), params=dict(key=self._apikey, token=self._token, fields=fields), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_board_field(self, field, idChecklist):
        resp = requests.get("https://trello.com/1/checklists/%s/board/%s" % (idChecklist, field), params=dict(key=self._apikey, token=self._token), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_card(self, idChecklist, actions=None, attachments=None, attachment_fields=None, stickers=None, members=None, member_fields=None, checkItemStates=None, checklists=None, limit=None, since=None, before=None, filter=None, fields=None):
        resp = requests.get("https://trello.com/1/checklists/%s/cards" % (idChecklist), params=dict(key=self._apikey, token=self._token, actions=actions, attachments=attachments, attachment_fields=attachment_fields, stickers=stickers, members=members, member_fields=member_fields, checkItemStates=checkItemStates, checklists=checklists, limit=limit, since=since, before=before, filter=filter, fields=fields), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_card_filter(self, filter, idChecklist):
        resp = requests.get("https://trello.com/1/checklists/%s/cards/%s" % (idChecklist, filter), params=dict(key=self._apikey, token=self._token), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_checkItem(self, idChecklist, filter=None, fields=None):
        resp = requests.get("https://trello.com/1/checklists/%s/checkItems" % (idChecklist), params=dict(key=self._apikey, token=self._token, filter=filter, fields=fields), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def get_checkItem_idCheckItem(self, idCheckItem, idChecklist, fields=None):
        resp = requests.get("https://trello.com/1/checklists/%s/checkItems/%s" % (idChecklist, idCheckItem), params=dict(key=self._apikey, token=self._token, fields=fields), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def update(self, idChecklist, name=None, pos=None):
        resp = requests.put("https://trello.com/1/checklists/%s" % (idChecklist), params=dict(key=self._apikey, token=self._token), data=dict(name=name, pos=pos))
        resp.raise_for_status()
        return json.loads(resp.content)

    def update_name(self, idChecklist, value):
        resp = requests.put("https://trello.com/1/checklists/%s/name" % (idChecklist), params=dict(key=self._apikey, token=self._token), data=dict(value=value))
        resp.raise_for_status()
        return json.loads(resp.content)

    def update_po(self, idChecklist, value):
        resp = requests.put("https://trello.com/1/checklists/%s/pos" % (idChecklist), params=dict(key=self._apikey, token=self._token), data=dict(value=value))
        resp.raise_for_status()
        return json.loads(resp.content)

    def new(self, idCard, name=None, pos=None, idChecklistSource=None):
        resp = requests.post("https://trello.com/1/checklists" % (), params=dict(key=self._apikey, token=self._token), data=dict(idCard=idCard, name=name, pos=pos, idChecklistSource=idChecklistSource))
        resp.raise_for_status()
        return json.loads(resp.content)

    def new_checkItem(self, idChecklist, name, pos=None, checked=None):
        resp = requests.post("https://trello.com/1/checklists/%s/checkItems" % (idChecklist), params=dict(key=self._apikey, token=self._token), data=dict(name=name, pos=pos, checked=checked))
        resp.raise_for_status()
        return json.loads(resp.content)

    def delete(self, idChecklist):
        resp = requests.delete("https://trello.com/1/checklists/%s" % (idChecklist), params=dict(key=self._apikey, token=self._token), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

    def delete_checkItem_idCheckItem(self, idCheckItem, idChecklist):
        resp = requests.delete("https://trello.com/1/checklists/%s/checkItems/%s" % (idChecklist, idCheckItem), params=dict(key=self._apikey, token=self._token), data=None)
        resp.raise_for_status()
        return json.loads(resp.content)

