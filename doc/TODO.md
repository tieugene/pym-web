# TODO

- [x] Settings
- [x] Store: LCRD
- [x] Store on/off
- [x] Filter
- [x] Entry: LCRUD
- [x] Sort
- [x] Store: U
- [x] Sitemap (dot)

## Fixme:
### Store:
- [ ] reload entries on store add/edit/del

### Entry
- [ ] dtstart/due tz (CU)
- [ ] store read-only[^1] (U)

## Polish:
### List:
- [ ] [CSS](https://idg.net.ua/blog/uchebnik-css)
- [ ] list:
  - [ ] prio: color
  - [ ] status: color
  - [ ] due: color
  - [ ] due: in_word
  - [ ] highlite mandatory/empty/filled/err
  - [ ] async iterator
- [ ] entry:
  - [ ] prio: += range (disabled on int empty or < 1)
  - [ ] progress: += range (disabled on int empty)
  - [ ] del: confirm ('sure?')

#### html:
- <placeholder>
- icons: svg sprite, font

## Issues:
- TodoList: select whole of row
- iterate over entries w/ kbd
- col2show, colorder - by names
- select Entry - invisibnle radio or select>option
- uuid for route [^2]
- find: ordered set:
  - OrderedSet < pip ordered-set
  - dict.fromkeys(keywords)
  - uniq list
- dark/light theme[^3]
- cProfile

### cgf:
- [ ] col2show: set[str]
- [ ] colorder: OrderedSet[str]
- [ ] showLeftPane
- [ ] showDetails

### pym-core:
- settings
- sync (builtin)
- git backend?

## Stores:

Name  | Path
------|-----
Cloud | `/Users/eugene/VCS/my/GIT/pyqtpim/_data/eap/ti.Cloud`
Fedora| `/Users/eugene/VCS/my/GIT/pyqtpim/_data/eap/ti.Fedora`
Job   | `/Users/eugene/VCS/my/GIT/pyqtpim/_data/eap/ti.Job`
Tasks | `/Users/eugene/VCS/my/GIT/pyqtpim/_data/eap/ti.tasks`
PR    | `/Users/eugene/VCS/my/GIT/pyqtpim/_data/pr/owncl`

[^1]: https://jsbin.com/jecerofuli/1/
[^2]: https://github.com/wbolster/flask-uuid
[^3]: https://css-tricks.com/a-complete-guide-to-dark-mode-on-the-web/
