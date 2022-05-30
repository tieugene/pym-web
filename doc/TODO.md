# TODO

- […] Sitemap (dot)
- [x] Settings
- [x] StoreList CRDL
- [x] Store on/off
- [x] Filter
- [ ] Sort: find like quicksort using lessThen
   *note: after filter*
- [ ] Entry:
  - [ ] C
  - […] R (== **details**): radio|select | ajax
  - [ ] U
  - [ ] D
  - [x] L: display handlers (*Flask custom filter*)

## Polish:
### List:
- prio.color
- status.color
- due.in_word
- dua.color
- summary.radio: hide

## Select entry:
- radio -> POST -> session(entry.uid)
- radio -> AJAX
- onclick() = function load_entry(uid) ([RTFM](https://www.delftstack.com/howto/javascript/load-html-file-javascript/))
- note: if uid in sessionthen can hichlitelist / clean details

## Settings:
- store: U
- json
- stores
- col2show: set[str]
- colorder: 

## Issues:
- col2show, colorder - by names
- select Entry - invisibnle radio or select>option
- uuid for route: https://github.com/wbolster/flask-uuid

### pym-core:
- settings
- sync (builtin)
- git backend?

prio:

- 9: darkblue darr;
