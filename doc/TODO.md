# TODO

- […] Sitemap (dot)
- [x] Settings
- [x] StoreList CRDL
- [x] Store on/off
- [x] Filter
- [ ] Sort [^1] *note: after filter*
- [ ] Store: U
- […] Entry:
  - [x] L
  - [x] R
  - [x] C
  - [x] D
  - [ ] U

## Polish:
### List:
- [ ] list:
  - [ ] prio: color
  - [ ] status: color
  - [ ] due: color
  - [ ] due: in_word
  - [ ] highlite mandatory/empty/filled/err
- [ ] entry:
  - [ ] prio: += range (disabled on int empty or < 1)
  - [ ] progress: += range (disabled on int empty)
  - [ ] del: confirm ('sure?')

## Settings:
- [x] store
- [x] json
- [x] stores
- [x] filter
- [ ] sort
- [ ] col2show: set[str]
- [ ] colorder: OrderedSet[str]
- [ ] showLeftPane
- [ ] showDetails

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

### pym-core:
- settings
- sync (builtin)
- git backend?

[^1]: [list.sort, sorted()](https://docs.python.org/3/howto/sorting.html)
[^2]: https://github.com/wbolster/flask-uuid
