import sys

import tv.weblog.db
import tv.weblog.output

print "initdb ...",
sys.stdout.flush()
tv.weblog.db.initDb()
print  "done"

#pprint(s.xmlStorageSystem.saveMultipleFiles('112292', '7548163f02a81b50385b4ed9f6e1f151', ['test.text'], ['blabla']))


def main():
    i = 1
    tv.weblog.output.renderItem(tv.weblog.db.getItem('7373200212100903073773'))
    tv.weblog.output.renderItem(tv.weblog.db.getItem('72482200212100902483772'))
    tv.weblog.output.renderItem(tv.weblog.db.getItem('48416200212091206413748'))
    for item in tv.weblog.db.getAllItemsByDate():
        tv.weblog.output.renderItem(item)
        i += 1
        if i == 50000:
            #    pass
            break

#import profile
#profile.run('main()')
main()
import tv.weblog.output.todo
tv.weblog.output.todo.commit()
tv.weblog.output.todo.commit()
