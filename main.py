#!/usr/bin/env python3
from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.RunScriptAction import RunScriptAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from pathlib import Path

class PassExtension(Extension):

    def __init__(self):
        super(PassExtension, self).__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):

    def on_event(self, event, extension):
        options = [filename for filename in Path.home().glob('.password-store/**/*.gpg')]

        if event.get_argument() is None:
            return RenderResultListAction([ExtensionResultItem(icon='images/icon.svg',
                                             name='Type to search',
                                             description='Password search is fuzzy',
                                             on_enter=HideWindowAction())])

        keyword = event.get_argument()
        candidates = []
        for opt in options:
            name = opt.relative_to(Path.home().joinpath('.password-store')).with_suffix('')
            name = '%s' % name
            if name == '_':
                continue

            # basic fuzzy string search
            rest = name[:]
            score = 0
            for char in keyword:
                find = rest.find(char)
                if find == -1:
                    # no match
                    continue

                # match!
                rest = rest[find+1:]
                score += 1
                if find == 0:
                    score += 1

            if score > 0:
                candidates.append((name, score))

        candidates = sorted(candidates, key=lambda c: c[1], reverse=True)
        items = []
        for (candidate, score) in candidates[:5]:
            items.append(ExtensionResultItem(icon='images/icon.svg',
                                             name='%s' % candidate,
                                             description='%s (match: %d)' % (candidate, score),
                                             on_enter=RunScriptAction("pass -c {}".format(candidate), None)))

        return RenderResultListAction(items)

if __name__ == '__main__':
    PassExtension().run()
