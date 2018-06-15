from Dataproviders.Fantasymassage import Fantasymassage

evil = Fantasymassage()
Entries = evil.getNewestEntries()

evil.getMetadata(Entries[1]['url'])