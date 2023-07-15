#enconding : utf-8
import copy
from os import remove
import pandas as pd
import re
import time
yuzhi = 0.05
StockSourceList = ['advfn', 'barchart', 'barrons', 'bloomberg', 'boston-com', 
    'bostonmerchant', 'business-insider', 'chron', 'cio-com', 'cnn-money', 'easystockalterts', 'eresearch-fidelity-com', 'finance-abc7chicago-com', 'finance-abc7-com', 'financial-content', 'finapps-forbes-com', 'finviz', 'fool', 'foxbusiness', 
    'google-finance', 'howthemarketworks', 'hpcwire', 'insidestocks', 'investopedia', 'investorguide', 'marketintellisearch', 'marketwatch', 'minyanville', 'msn-money', 'nasdaq-com', 'optimum', 'paidcontent', 'pc-quote', 'personal-wealth-biz', 
    'predictwallstreet', 'raymond-james', 'renewable-energy-world', 'screamingmedia', 'scroli', 'simple-stock-quotes', 'smartmoney', 'stocknod', 'stockpickr', 'stocksmart', 'stocktwits', 'streetinsider-com', 'thecramerreport', 'thestree', 'tickerspy', 'tmx-quotemedia', 'updown', 'wallstreetsurvivor', 'yahoo-finance', 'ycharts-com', 
    'zacks']
FlightSourceList = ['aa', 'flightexplorer', 'airtravelcenter', 'myrateplan', 'helloflight', 'flytecomm', 'flights', 'businesstravellogue', 'flylouisville', 'flightview', 'panynj', 'gofox', 'foxbusiness', 'allegiantair', 'boston', 'travelocity', 'orbitz', 'weather', 'mia', 'mytripandmore', 'flightarrival', 
'flightaware', 'wunderground', 'flightstats', 'quicktrip', 'world-flight-tracker', 'dfw', 'ifly', 'ua', 'ord', 'usatoday', 'CO', 'flightwise', 'iad', 'den', 'sfo', 'mco', 'phl']

BookSourceList = ['eCampus.com', 'Indoo.com', 'textbookxdotcom', 'A1Books', 'textbooksNow', 'paperbackworld.de', 'Caiman', 'Movies With A Smile', 
'Marando.de Versandbuchhandlung', 'AHA-BUCH', 'Versandantiquariat Robert A. Mueller', 'Morgenstundt Buch & Kunst', 'AlphaCraze.com', 'Odeon Books', 
"Powell's  Books", 'Quartermelon', 'Browns Books', 'Books Down Under', 'SWOOP', 'TheBookCom', 'THESAINTBOOKSTORE', "Mellon's Books", 'Blackwell Online',
'Stratford Books', 'The Book Depository', 'Englishbookservice.com GTI GmbH', 'Revaluation Books', 'Papamedia.com', 'FREE U.S. AIR SHIPPING @ thebookcompany', 
'Bobs Books', 'Gunars Store', 'Gunter Koppon', 'Limelight Bookshop', 'MildredsBooks', 'BEST BARGAIN BOOKS', 'OPOE-ABE Books', 'Players Quest', 'AshleyJohnson', 
'happybook', 'ben artoge bookstore', 'Schmidsche Buchhandlung Fachbuch', 'Technischer Overseas Pvt. Ltd.', 'ReadMate', 'The E', 'EnjoyStudy', 'BookJoe', 'HTBOOK', 
'Sunmark Store', 'softcoverdeal', 'Books2Anywhere.com', 'Paperbackshop-US', 'Striped Ostrich', 'Deepak Sachdeva', 'flybookstore', 'Bookmantra.com', 'Briggs Books', 
'Oxfam Bookshop Hertford', 'aa42.com', 'ROBINART BOOKS', 'Cody Books Ltd', 'James & Naomi Cummings, Booksellers', 'Sandy Chong', 'Nancy McMath',
'Hein & Co. Used and Rare Books', 'International Books', 'allenac', 'BOOKFORYOU', 'BetterWorld.com', 'Better World Books Sale', 'a2zbooks', 'Pay Less Books Malaysia',
'Pioneer Book', "Sam Weller's Zion Bookstore, ABAA", 'Govind Garg', 'Cobain LLC', 'TextSearch, International (We Recycle!)', 'Book Gallery // Mike Riley', 'Livrenoir',
'Bunches of Books', 'Books R us', 'Bookworms, Inc.', 'Booksoul', 'Collegebooksdirect.com', 'CollegeTextbookBin.com', 'BookHolders', 'Campus Book Store', 'xpresstext', 
'DVD Legacy', 'Economy Books', 'Ham Books', 'Borgasorus Books, Inc', 'Bookbyte / Norwest Textbooks', 'Mayapapaya Books', 'PsychoBabel Books & Journals', 'Books on the Web',
'Great Buy Books', 'Cultured Oyster Books', "Hikah's Books", 'Recycle Bookstore', 'Fellowshipbooks.net', 'GREAT_TEXTS', 'Black Swan Books', 'Book Journeys', 
'Kentish Knock Company', 'Frugal Media', '51textbooks', "JULIAN'S BOOKS", 'Abyssbooks', 'Inkt', 'Inkt - Free UK Shipping 1st Class', 'GotBooks', 'Hippo Books', 
'AarenLLC', 'The Bookman', 'MesaBookSales', 'LGTextbooks.com', 'Majaka Books', 'Alexander Gallery', 'www.textbooksintl.com', 'S M Inc', 'Books In The City, Inc.', 
'AAAbooks4u', 'Eco Encore', 'CalibanBooks Pittsburgh PA, ABAA', 'COBU GmbH & Co. KG', '5559store', 'ProService', 'www.textbooksrus.com', 'brandnewtextbooks', 
'Missionbooks', 'Alinonline', 'A Team Books', 'Bingo Books', 'Orbidoo.de', 'Balkanika Online', 'SCIENTEK BOOKS', 'SnowLionBooks', 'OwlsBooks', 'thriftbooks.com', 
'Beagle Books', "Doug's Top Hat Computer Books", 'isedeals', 'HJP WISSENSCHAFTL. VERSANDBUCHHANDLUNG', 'Bradbooks', 'Fachbuecher Weltversand', 'Actinia Bookstores', 
'Kitabay', 'morebooks2', 'Phatpocket Limited', "Henry's Biz Books", 'Annex Books Inc', 'Cornwall Discount Books', 'Orca Books', 'Textbook Recycling Co.', 
'Textbooks For Less', 'California Textbooks', 'MORGANA INC', "Laura's Rare Books", 'Mandala Books', 'Harbor Book Cellar', 'FredsBookHouse', 'Gallowglass Books', 
'Russell Books', 'Oddball Books', 'e-Book Traders, Inc.', 'UniversalAthenaeum', 'Memicky', 'Allichar Books', '>> MIDWEST BOOK COMPANY <<', 
'Gail P. Kennon, Book-Comber', 'Safe Harbor', 'TranceWorks', 'Bookpeople of Moscow', 'Limebay Books', 'BookSmart', 'JOOT Just Out Of Time', 
'Hoxton Book Depository', 'Swan Trading Company', "Woody's Books", 'The Possible Dream company', 'Ensight Book Services', 'Griffin Books', 
'Jacaranda Online', 'Bill Dias, Bookseller', 'William H. Allen Bookseller', 'heather jo frey, bookseller', 'Booklibrary', 'Valerie Dzendzeluk', 'Ion Fine Books', 
'Textbook Brokers', 'G.T.S.', 'Back Alley Books', 'BYOtB college textbook store', 'Looking for Books?', 'Tacoma Book Center', 'Kayleighbug Books', 'Kayleighbug', 
'Leaf-E-Lady Books', 'Ship Today Books', 'PARKER-FOX LLC Books', 'D & A Worldwide Textbook Service', 'Bargainbookstores.com', 'Wonder Book', 'JESSEBOOK', 'Booksavers', 
'Pro Quo Books', 'Books: Silver Rose LLC', 'tombargainbks', 'Title Wave Books', 'Garter Books', '50000BOOKS.com', 'Awesome Books', 'pasargad bookstore', 
'BookBuyers OnLine', 'Gulls Nest Books, Inc.', 'Book Baron Anaheim', 'Book Emporium', 'Highfield Book Shop', 'Arvelle Buch- und Medienversand', 'Abraxus Books', 
'Nationwide Book Traders', 'College Book Service', 'Price Cut Books Ltd', 'Monarchy books', 'mediasell (G.I.V. mbH)', 'TorontoDirect', 'Total Information', 
'Books @ El Paso', 'Gildonbooks', 'Zillions OF', 'Noram International Partners, LLC', 'Pacific Book Exchange, LLC', 'Mostly Books', 
'Bookdonors Community Interest  Co Ltd', 'The Book Cellar, LLC', 'Frugal Media Corporation', '! TextbookAce.com!', 'Empire Booksellers', 
'Urbano Libros', '>>>Metro Books>>>', 'Dynes Investments LLC', 'Textbook Recycle', 'BOOKMASTERS', 'Kirk Bayless', 'Hyannisport Books', "Avol's Bookstore", 
'FrogPrinceBooks', 'Oak Creek Books', 'WAP Central Booker', 'Glued To The Tube Books', 'TenBestBooks.com', 'Maher The Bookseller BA', 'James Sroda - Books', 
'Bananafish Books', 'By Hand Books', 'Seashellbooks.com, Inc.', 'AWOC.COM', "Scholar's Book Outlet", 'Much Ado About Books', 'AAA Textbooks', 'Piedmont Books', 
'Book Mavericks', 'Bookfanz', 'Antiquariat an der Universit?t Darmstadt', 'Lucky Books', 'Brian t stoval', 'Blumenkraft Books', 'Samkat Books', 'Usedbooks123', 
'Free Shipping Books', 'Ginny6 Books', 'Librairie Antoine', 'Heroic Image', 'YES BOOKS, Inc,', 'DurnickBooks', 'Black and Read Bookstore', 'Archives Books, Inc.', 
'Calvello Books', 'susan bookshop', 'Mole de Books', 'Books for Change', 'PBX WAREHOUSE LLC', 'b2books', 'George Cross Books', 'Greenview Book Depository', 
'Allison B. Goodsell, Rare Books', 'Manchester By The Book', 'Centurion Books', 'International Publishers Group', 'Book Liquidators', 'The Green Jacket', 
'Flyingelfbooks', 'Rocking Chair Books', 'Gemstone Books', 'Nelson & Nelson, Booksellers', 'BooksR4U', 'RecycleBooks.ORG', 'The Avocado Pit', 'Books Beyond Borders', 
'Woodward Books', 'Bulldogbooks', 'Pavillion IV Books', "Lawrence's Books", 'Twice Read Books', 'Rare Finds Books, Music, Etc.', 'BookZone Illinois', 
'Jerome McCarthy', 'bookscorner1', 'Mybooklocator', 'Shadow Books', 'The BiblioFile', 'Foolscap Books', 'www.BlueCrestBooks.com', 'Lost Books', 'Bookman', 
'Turn of the Century', 'PaceSetter Books', 'BookOrders', 'David M. Riley', 'BooksRUs.biz', "Veda's Books N More", 'VeryCoolBooks.com, Inc.', 'park boulevard books',
'Lucky Dog Books', 'Brettsbooks', "Marilyn's Attic", 'Charles Berry, Bookseller', 'HRS Books', 'Smith Family Bookstore', 'Full Circle Books', 'Junic Resources', 
'cheapbookshop', 'Jefeducator', 'Book Booth', 'Fireside Angler', 'totalqualitybooks', 'R. C., Bookseller', 'Charles River Bookshop', 'Louis Morin',
"Diane's Books and  Novelties", 'NYCprice', 'Recycled Pages', 'JR Books', 'Dave Henson - Books', 'Hound Dog Books', 'bingobooks2', 'Silicon Valley Fine Books', 
'University of Leicester Bookshop BA', 'Pengwyn Books, Ltd.', 'Book Barn Ltd', 'C. Angela Wykoff, Bookseller', 'Mary Jane Books', 'Chandler & Wright', 'Lawson Books', 
"TJ's Books", 'AGD Books', 'Aardvark Books', 'The Book Centre', 'RhinoPlus.net', 'Sandra Gudac', 'Half Red House', 'Elistics', 'Jim Camden', 'You Need This, LLC', 
'Hanselled Books', 'JR TRADING/BOOKJOINT', 'CambridgeBookstore.com', "Beazle's Books", 'Brockport College Foundation -- Books', 'Benton Books', 'Alfa Bookstore', 
'Normal Books', 'Rivalbooks.com', 'Sheebook', 'Infinity Books Japan', 'Calliope Books', "HoneyBee's Books", "Reader's Corner, Inc.", 'The Book Stop', 
'Magus Books Seattle', 'OmniBooksUK Ltd', 'Curio', 'Northshore Tech Sales Inc', 'More Books, Please', 'The Big Book Sale', "Rack 'em Books", 'Thomas E Franklin', 
'Cellar of Books', 'Avept', 'The Book Shelf LI', 'Rowinski books', 'Bound Matter', 'JE Duplice Books', 'Chestnut Tree Books', 'Taradise Books', 'BOOKS ENTERPRISE', 
'First Used Books', 'Calliope Bookstore', 'BaBooNeez', 'ExtremelyReliable', 'Oak Hill Books of Austin', 'The Dragon Fruit Garden', 
'Barter Books', 'The Book Place', 'University Book Source, Ltd.', 'Affordable Collectibles', 'Art Solo', 'Robin Summers', 'Pulpfiction Books', 'bluecoatbooks.co.uk', 
'Jenson Online', "David's Books", 'Rainbow Bear Books and Miscellaneous', "Comstock's Bindery and Bookshop", 'Reuben Goldberg Books', 'Bookarama, Inc', 'Zubal Books', 
'BigCat Books', 'ACSBOOKS.COM', 'A Novel Idea Bookstore', 'Friends of the San Carlos Library', 'R D Greenberg', 'elordinc', 'Strand Book Store, ABAA', 
'Furniture Recycled Ltd', 'Religious Books', 'Books For Trees', 'PCS books', 'Highway Book Shop', 'YesterYear Books', 'The Haven Bookstore', 'UK Internet Books', 
'okin books', 'T. B. Anderson', 'West CR Books', 'The Book Broker', 'book-recycler.com', 'Orchid Books', "Beck's Books of Sacramento", 'BEJ Ent.-Online Bookstore', 
'OOPLAS', 'Teen LEEP', 'VielBuch.de - Onlineantiquariat', 'PIMA', 'LDS Heritage Books', 'dixieland books', 'Harbor Isle Books', 'Wise Owl Books', 'MalibuEvenings', 
'Crazy Ladies Bookshop', 'ELEPHANTBOOKS.COM', 'Bookworm Exchange', 'Left Coast Books', 'ADSRUS INC.COM', 'FOREST BOOKS', 'Books From California', 'Hawk Books', 
'Experienced Books, LLC', 'www.anybookworld.com', 'BOOK EDDY', 'Booktopia', 'Acquired Books', 'Shop in Your Pajamas', "Ophelia's Books", 'LeChayim', 
"K&R's FIRSTEDITIONS", 'PlumCircle', "Chanda's Bargain Books", 'Alhambra Books', 'Bin Around The World', 'Dan Behnke Bookseller', 'Telegraph Books', 'Cummings Books', 
'Goldyne', 'Monroe Vista Group', 'Bookshop on the Avenue', 'flickswap.com llc', 'Kelvin Books', 'G3 Books', 'THE BOOK BIN -- ATTN: Carl', 'Plurabelle Books', 
'Antiquariat Mehlig', 'Treasure Coast Books', 'Warrior Books, Inc.', 'P.C. Schmidt, Bookseller', 'COMPUTER BOOK WORKS', 'Early Republic Books', 
'Gene Carpenter, Bookseller', 'Metropolitanbookstore', 'Great Northwest Bookstore', 'Sterling Books A.B.A. I.L.A.B.', 'Davids Antiquariat + www.catch-a-book.de', 
'Elizabeth Brown Books & Collectibles', 'Mt. Baker Books', 'Willow Books', 'Larry Christian DBA  metoyoubooks', 'DCbooks', 'Chapterhouse Books Online BA', 
'The Bookman, Inc.', 'MACJULISON', 'Hay-on-Wye Booksellers', 'A. Raj Din-Dayal Booksellers', 'Hay-on-Wye Booksellers2', 'Tjeerd Dijkstra', 'Indian Path Books', 
'Enviro-Text Books, Inc.', 'BookLovers.co.uk', 'DustJacketBooks', "Gail's Books", 'Prairie Archives', 'UPSTATE BOOKS', 'The Book Keeper, LLC', 'Summer House Books', 
"Carol's Books", 'Jubilee Books', 'BOOKPOWER', 'Three Spires Books', 'Monk Cabin Books', 'These Old Books', 'Book Oasis', 'Pamplemousse Books', 'AB Book Company', 
'Luv them books', 'Northbrae Books', 'Quickshipment', 'Bank of Books', 'Beach Books', 'Ahab Books', 'Beacon Hill New Used and Rare Books', 'Keeps Books', 
'MikNik Books', 'New Boston Fine and Rare Books', 'Rose Bonaparte', 'Downtown Books and Beans', 'BOOKS MORE HANDSOME Than Fine', 'Ashcrest Books', 'Khare Enterprises', 
'Bluegrass Book Supply', 'ZEEBA Books', 'mannin books', 'Hometown Books', 'Livres Bronx Books', 'The Book Source', 'Reliable Enterprises, Inc.', "Lilly's Books", 
'Recycle Bookstore West', 'Minster Books', 'The Book Bin', "Dale's Books", 'The Book Escape', 'Bucklin Hill Books', 'Dawn Treader Bookshop', 'BookFargo', 'Chaineys', 
'ER Books', 'BridgeTown Books', "Mary's Creek Books", 'Collect Musings', 'Magers and Quinn Booksellers', 'Arundel Books', 'BeacyBooks', 'Out of Print', 
'Michael McCarty Fine Books', 'Adagio Books', 'Spine and Crown', 'Book Buzzard', 'Becauseyouread', 'bookslover11', 'Kalpatru LLC', 'textbook18', 'Keen Northwest', 
'Marbus Farm Books', "Anaximander's Bookshelf", 'Ted George', 'Alexandria Books', 'TextbookXPres', 'VERITASNOW', 'Eastburn Books', 'McAllister & Solomon Books', 
'FAB BOOKS', 'Desktop Music, LLC', "Lady Lisa's Bookshop", 'Bigdahn', 'GREAT PACIFIC BOOKS', 'Little Book Buddy', 'The Library Store', 'Book Peddler', 
'Yella-Umbrella Limited', 'Book Dispensary', 'buecherdackel', "Shirley's Book Services", 'Tuttle Bookstore', 'Remi Leclerc', 'Brillig Books', 'Bookman-Huntington', 
'midnight bookman', 'leifbooks', "Birkitt's Books", 'Jonathan Grobe Books', "Boomer's Books", 'Uwantthisbook', "Gusdorf's Books", 'badrisbooks', 'One Price Books', 
'Fishpond Limited', 'Diatrope Books', 'The Warm Springs Book Company', 'arbour books', 'pat marketing', 'Speedy Books shipping from USA!', 'Reliable Book Service', 
'Best Book Deals', 'boox2relyon', 'market4books', 'Daylight Books', 'Covenant International Inc.', 'BradsBooks.Com', 'HPC Publishers', 'John Gargiso', 'Northeast Books', 
'BookCloseOuts.com', 'avidbookseller', 'JoNa Books', 'Aamstar Bookshop', '-The Recycled Book Shop-', 'save_you_a_lot', 'RK Sellers', 'studentbookstoreglobal', 
'River City Books, LLC', 'Conover Books', 'Antiquariat Dorner', 'bookmac', 'Wolfcreek Books', 'Allen Williams Books', "Ruby's Market", "Elder's Bookstore", 
'J.E. MILES, A BOOKSELLER', 'Fairy Godmothers', 'the annex', 'DERBOOK', 'Goodale Enterprise', "Louisville's Book.Net", 'Classic Books Of Virginia', 'Briarwood Books', 
'Keva Books, LLC', 'Outspoken & Relaxed Reader Cafe', "Samm44's Used Books", 'Pandora Antiquariat', 'Philadelphia Book Company', 'Red Barn Books', 
'Antiquariat Kisch & Co.', 'RBR BOOKS', 'Mustardseed Enterprises', 'River Valley Books', 'THE OLD LIBRARY SHOP', 'The Used Bookstore', 'Books on the Boulevard', 
'ABC Books', 'Frabjous Books', 'The Book Den, ABAA', 'Book Lovers USA', 'LAKESIDE BOOKS', 'FREE POSTAGE ! @thebookcompany', 'SARL Culture-Factory', 
'Ecobook - Libreria del Economista', 'Mini City Media', 'Mega Media Depot', 'WorldOfBooks', 'Jimmy LaRue', 'Librairie La Canopee. Inc.', 'WebBookStore', 
'VENTURA PACIFIC LTD Out of Print Books', 'JUSTICE BOOK COMPANY', 'D2D Books', 'The Book Trader', 'Helion & Company Ltd', 'BookFargo C/O Christopher Roman', 
"Cassidy's  Bookstore", '86 Books', 'DotCom Liquidators / DC 1', 'Ulrich Books, LLC', 'Bookbox', "Scholar's Basement", 'EBOOKMINE', 'B?cher Th?ne', 
'Wonder Book and Video', 'Get Used Books', "Bailey's Books", 'The Book Store', 'Creative Outlet', 'lorraine leaton', 'Books Express', 'Oakwood Books/ EMB Triad', 
'MoonXscape', 'MindFair', 'Tomes in the Attic', 'Changing Hands Bookstore', 'Astley Book Farm', 'Der Buchfreund', 'Chris Duggan, Bookseller', 'BookPenny', 
'macysbook', 'the text book planet. com', 'Gurung Prem Kala', 'yello  textbook', 'cheaptext4u', 'Market Media', 'The CollegeStore 207', 'SUBtext', 
'The Aleph', 'Chicago Textbook, Inc.', 'bookbrothers.net', 'DirtCheapBooks4u', 'vismum', 'ValoreBooks', 'Church Stretton Books', 'Au brouillon de culture', 
'Wm Burgett Bks and Collectibles', 'B-Line Books', 'Blue Fog Books', 'sapientia', "Aristotle's  Library", 'xiao xiaohong', 'The Second Reader Bookshop', 
'Carnforth Bookshop BA', 'Laird Books', 'Eric T. Moore Books', 'Chamblin Bookmine', 'Burke Used Books', 'SUNSET BOOKS', 'AABooks', 'BPC Books', 
'The Critical Eye Used Books', 'booksmart', 'Book Buyers', 'FirstClassBooks', 'Read-A-Book', 'Summerlee Books', "Charlie Byrne's Bookshop", 
'PONCE A TIME BOOKS', 'kbooks', "Baldwin's Book Barn", 'NETOCC', 'Twice Sold Tales', 'ReadingStore', 'The Book Fiend', 'Barbara Anderson', 'Book Nook of Orange County', 
'Book Source', "ODonnell's General Store", 'Paperback Emporium', 'CARLO BARONCINI', 'Victoria Bookshop', 'AZBOOKA', 'Bookstir', 'Utah Book and Magazine', 'Oxbooks', 
"Thomas F. Pesce'", 'Red Carpet Books', 'Purplefishbooks', 'Goulds Book Arcade, Sydney', 'Tudorbooks', 'Abba Books', 'Pride and Prejudice-Books', 
'Robert S. Brooks, Bookseller', 'William A. Breitmaier', 'Twice Sold Tales Queen Anne', 'Defunct Books', 'Steamer Trunk Books', 'Mor-books', 'IHS ATP', 
'www_mediastuffs_com', 'Warnock Books', 'Seattle_Bookseller', 'stephanie henry', 'One Man Operation Bookseller', 'mycheapbooks', 'skyvalleybooks', 'Walrus Books', 
'Old Orchard Bookstore', 'A New Life Books', 'looksgoodbooks', 'SAIEIS INC', 'Finger Lakes Cottage', 'Philip Weiss Auctions', 'Global Book Locator', 
'Scrooge and Marley Books', 'The Book Faire', 'Gold Chest Books', 'Paper Moon Books', 'Forgotten Treasures', 'Novanglus Books', 'ReadingByCoastal', 
"Veda's Marketing Agencies", 'www.icehousebooks.co.uk', 'RWL GROUP  (Booksellers)', 'Tiber Books', 'ForgottenFinds- Bookseller', 'Book Planet', 'Blue Sage Books', 
'DIANE Publishing Co.', 'Northside Book Market Used & Rare', 'Still Water Books', 'Timothy J. Brancamp, Bookseller', 'Bridebooks, LLC', 'Fairandfast', 
'MY Back Pages Balham', 'Brownsbooks International', 'Elaine Thompson', "Oxfam - SU Students' Union Branch", 'Academic books online', 'Innana Rollason', 
'Research Ink', 'GALLOWAY AND PORTER LTD ABA ILAB  BA', 'J. HOOD, BOOKSELLERS,    ABAA/ILAB', 'NewtonLibrary.net', 'Voyager Books', 
'Leader Books SA', "Michael's Books", 'E. Louis Hinrichs', 'Virtuous Volumes et al.', 'Backwater Bookstore', 'Atticus Books', 'North Mountain Books', 
'Riverby Books', 'Bibliohound', 'Lorem Ipsum Books', 'Paradise Found Books', 'Banjo Booksellers, IOBA', 'General Eclectic Books', 'Sharon Neva Book Trader', 
'Bookstore at the End of the Universe', 'Charles Bossom', 'Dana Books', 'Readerfind Booksearch', 'Harvest Book Company', 'Bibliotique', 'Fairlane Books', 
'Skoob (Russell Square)', 'Winged Monkey Books', 'Neil G. Marshall', 'Primrose Hill Books BA', 'aridium internet books', '100POCKETS', "YoYo's Books", 
'A Squared Books (Don Dewhirst)', 'Kennys Bookshop and Art Galleries Ltd.', 'JML Books', 'Hill Country traders', 'BWalder', 'www.arcanabooks.us', 
'Books on High/Tri-Village Book Company', 'SalesOn', 'Finisterre Books', 'Countless Pages Book Store', 'Live Oak Books', 'Old Goat Books', 'Lindsay Family Books', 
"Tom's Used Books", 'Textbook Master', 'CyberSmith Books', 'books4u31', 'Squirrel Away Books', 'Bridge Books, Inc.', 'BestPricedBooks.net', "Burke's Books", 
'Technical Book Site', 'The Muse BA', 'Kenneth Biggs', "Q's Books", 'Lake Macquarie Secondhand Books', 'Puddle Books', 'All Books Inc.', 'A Good Read, LLC', 
'BookRunner Ltd', 'John Adams Bookshop BA', 'Leura Books', 'Michael Stein Versand-Antiquariat', 'cheap textbook', 'Books & Videos Worldwide', 'George Longden', 
'Endeavour Books', 'COLORBOOKS2006', 'Michael  mcVay', 'Harvard Book', 'Michael Cunningham, Bookseller', 'Reedmoor Books', 'Textbook Recyclers', "Leon's Book Store", 
'Forthway Books', 'Rose and Laurel Bookshop', 'Crossroad Books', 'Antiquariat Thomas Haker', 'Oxfam Shop - Liverpool', 'RON RAMSWICK BOOKS']
#region 无用函数
# def FComputeThreeEstimates(ClaimData,SourceList,QuestionRow,Lambda,ClaimNameRow):
#     StartRowList = [2]
#     EndRowList = []
#     ThreeEstimatesValueList = []
#     name = ClaimData[ClaimNameRow][2] #sial
#     #print(name)
#     for i in range(ClaimData.shape[0] - 2) :
#         if ClaimData[ClaimNameRow][i + 2] != name:
#             EndRowList.append(i + 1)
#             StartRowList.append( i + 2)
#             name = ClaimData[ClaimNameRow][i + 2]
#     EndRowList.append(ClaimData.shape[0] - 1 )

#     TruthWorthList = [0.8] * len(SourceList)
#     ConfidenceMatrix = [['initial' for col in range(len(SourceList))]for row in range(len(EndRowList))]  
#     ClaimSourceMatrix = [['initial' for col in range(len(SourceList))]for row in range(len(EndRowList))]  #记录每个Claim是谁说的
#     SourceClaimMatrix = [['initial' for col in range(len(SourceList))]for row in range(len(EndRowList))]  #记录每个Source说了什么
#     ErrorFactorMatrix = [['initial' for col in range(len(SourceList))]for row in range(len(EndRowList))]  

#     for i in range(len(EndRowList)):
#         for j in range(EndRowList[i] - StartRowList[i] + 1):#因为每个s只有一个c,所以ClaimSourceMatrix、SourceClaimMatrix、ConfidenceMatrix和ErrorFactorMatrix都是一样大的
#             print(EndRowList[i] - StartRowList[i] + 1)
#             ClaimSourceMatrix[i][j] = ClaimData[ClaimNameRow -1][j + StartRowList[i]]
#             SourceClaimMatrix[i][j] = ClaimData[QuestionRow][j + StartRowList[i]]
#             ErrorFactorMatrix[i][j] = 0.1
#             ConfidenceMatrix[i][j] = 0
#     for i in range(len(EndRowList)):
#        while(1):
#             if 'initial' in ConfidenceMatrix[i]:
#                 ClaimSourceMatrix[i].remove('initial')
#                 SourceClaimMatrix[i].remove('initial')
#                 ErrorFactorMatrix[i].remove('initial')
#                 ConfidenceMatrix[i].remove('initial')
#             else:
#                 break
                   
#     InterNum = 0
#     while (1):#repeat
#         InterNum += 1
#         TempTruthWorthList = copy.deepcopy(TruthWorthList)
#         for i in range(len(EndRowList)):#for d ∈ D
#             for j in range(EndRowList[i] - StartRowList[i] + 1):# for v ∈ Vd
#                 Pos = 0
#                 Neg = 0
#                 v = SourceClaimMatrix[i][j]
#                 for ii in range(len(ClaimSourceMatrix[i])):# 遍历Sd
#                     if SourceClaimMatrix[i][ii] == v: # s ∈ Sv
#                         Pos += 1 - TruthWorthList[SourceList.index(ClaimSourceMatrix[i][ii])] * ErrorFactorMatrix[i][ii]
#                     else: # s ∈ S-v
#                         Neg += TruthWorthList[SourceList.index(ClaimSourceMatrix[i][ii])] * ErrorFactorMatrix[i][ii]
#                 ConfidenceMatrix[i][j] = (Pos + Neg) / (EndRowList[i] - StartRowList[i] + 1)
#             ConfidenceMatrix[i] = NormalizeList(ConfidenceMatrix[i],Lambda)
            
#         for i in range(len(EndRowList)):#for d ∈ D
#             for j in range(EndRowList[i] - StartRowList[i] + 1):# for v ∈ Vd
#                 Norm = 0
#                 Pos = 0
#                 Neg = 0
#                 v = SourceClaimMatrix[i][j]
#                 for ii in range(len(ClaimSourceMatrix[i])):# 遍历Sd
#                     if TruthWorthList[SourceList.index(ClaimSourceMatrix[i][ii])] != 0: # Ts != 0
#                         Norm += 1
#                         if SourceClaimMatrix[i][ii] == v: # s ∈ Sv
#                             Pos += (1 - ConfidenceMatrix[i][j]) / TruthWorthList[SourceList.index(ClaimSourceMatrix[i][ii])]
#                         else:# s ∈ S-v
#                             Neg += ConfidenceMatrix[i][j] / TruthWorthList[SourceList.index(ClaimSourceMatrix[i][ii])] 
#                 ErrorFactorMatrix[i][j] = (Pos + Neg) / Norm
#             ErrorFactorMatrix[i] = NormalizeList(ErrorFactorMatrix[i],Lambda)

#         for i in range(len(SourceList)):# for s ∈ S
#             Norm = 0
#             Pos = 0
#             Neg = 0
#             s = SourceList[i]
#             for j in range(len(EndRowList)):
#                 if s in ClaimSourceMatrix[j]:# d ∈ Ds
#                     for ii in range(len(ClaimSourceMatrix[j])):
#                         if ClaimSourceMatrix[j][ii] == s and ErrorFactorMatrix[j][ii] != 0:
#                             Pos += (1 - ConfidenceMatrix[j][ii]) / ErrorFactorMatrix[j][ii]
#                             Norm += 1
#                         else:
#                             if ErrorFactorMatrix[j][ii] != 0:
#                                 Neg += ConfidenceMatrix[j][ii] / ErrorFactorMatrix[j][ii]
#             if Norm == 0:
#                 continue
#             TruthWorthList[i] = (Pos + Neg) / Norm
#         TruthWorthList = NormalizeList(TruthWorthList,Lambda)

#         #检查是否收敛
#         v0 = list(map(lambda x: abs(x[0]-x[1]), zip(TruthWorthList, TempTruthWorthList)))
#         if max(v0) < yuzhi or InterNum == 100:
#             if InterNum == 100:
#                  print("第",QuestionRow - ClaimNameRow,"个问题无法收敛")
#             break
#     #结束repeat
#     for i in range(len(EndRowList)):
#         ThreeEstimatesValueList.append(SourceClaimMatrix[i][ConfidenceMatrix[i].index(max(ConfidenceMatrix[i]))])  
                
#     return ThreeEstimatesValueList

# def FThreeEstimates(SourceList,ClaimData,QuestionKindNum,ClaimNameRow,TruthValueMatrixDataStorePath):
#     ClaimNameList = []
#     #这里的2是为了去除前两行的行标等
#     print("3-Estimates is working")
#     for i in range(ClaimData.shape[0] - 2):
#         if ClaimData[ClaimNameRow][i + 2] not in ClaimNameList:
#             ClaimNameList.append(ClaimData[ClaimNameRow][i + 2])
#     ThreeEstimatesValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(ClaimNameList))]  
#     for i in range(len(ClaimNameList)):
#         ThreeEstimatesValueMatrix[i][0] = ClaimNameList[i]    
#     for i in range(QuestionKindNum):
#         print("Num",i+1,"Question")
#         ValueList = ComputeThreeEstimates(ClaimData,SourceList, i + ClaimNameRow + 1,0.5,ClaimNameRow)
#         for j in range(len(ThreeEstimatesValueMatrix)):
#             ThreeEstimatesValueMatrix[j][i + 1] = ValueList[j]
#     df = pd.DataFrame(ThreeEstimatesValueMatrix)#list不能直接转为excel，需要先转为DataFrame
#     df.to_excel(TruthValueMatrixDataStorePath,sheet_name='data1',na_rep='空值')
#     print("3-Estimates ends")
#     return ThreeEstimatesValueMatrix
#endregion

def NormalizeList(NeedNormalizeList,Lambda):#这边的归一化和论文中定义不一样
    if len(NeedNormalizeList) == 1:
        return NeedNormalizeList
    MaxList = max(NeedNormalizeList)
    MinList = min(NeedNormalizeList)
    if MinList == MaxList:
        return NeedNormalizeList
    #print(NeedNormalizeList,MaxList,MinList)
    # for i in range(len(NeedNormalizeList)):
    #     Value1 = (NeedNormalizeList[i] - MinList)/(MaxList - MinList)
    #     Value2 = round(NeedNormalizeList[i])
    #     NeedNormalizeList[i] = Lambda * Value1 + (1 - Lambda) * Value2
    for i in range(len(NeedNormalizeList)):
        NeedNormalizeList[i] = (NeedNormalizeList[i] - MinList) / (MaxList - MinList)
    return NeedNormalizeList

def CompThreeEstimates(ClaimData,SourceList,QuestionRow,Lambda,ClaimNameRow):
    StartRowList = [2]
    EndRowList = []
    QuestionRowNumList = []
    ThreeEstimatesValueList = []
    name = ClaimData[ClaimNameRow][2] #sial
    rank = 0
    #print(name)
    for i in range(ClaimData.shape[0] - 2) :
        if ClaimData[ClaimNameRow][i + 2] != name:
            EndRowList.append(i + 1)
            StartRowList.append( i + 2)
            name = ClaimData[ClaimNameRow][i + 2]
            QuestionRowNumList.append(rank)
            rank = 1
        rank += 1
    EndRowList.append(ClaimData.shape[0] - 1 )
    QuestionRowNumList.append(EndRowList[-1]-StartRowList[-1] + 1)

    TruthWorthList = [0.8] * len(SourceList)
    ClaimNoRepeaMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ]#有|c|列
    SourceNoRepeatMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ]#有|s|列
    ErrorFactorMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ] # 有|c|列
    ConfidenceMatrix = [['initial'for row in range(1)]for col in range(len(EndRowList)) ] #有|c|列
    for i in range(len(EndRowList)):
        for j in range(EndRowList[i] - StartRowList[i] + 1):
            if ClaimData[QuestionRow][StartRowList[i]+ j] not in ClaimNoRepeaMatrix[i]:
                ClaimNoRepeaMatrix[i].append(ClaimData[QuestionRow][StartRowList[i]+ j])
                ConfidenceMatrix[i].append(0)
                ErrorFactorMatrix[i].append(0.1)
            if ClaimData[ClaimNameRow - 1][StartRowList[i]+ j] not in SourceNoRepeatMatrix[i]:
                SourceNoRepeatMatrix[i].append(ClaimData[ClaimNameRow - 1][StartRowList[i]+ j])
    for i in range(len(EndRowList)):
        ClaimNoRepeaMatrix[i].remove('initial')
        SourceNoRepeatMatrix[i].remove('initial')
        ErrorFactorMatrix[i].remove('initial')
        ConfidenceMatrix[i].remove('initial')
       
    InterNum = 0
    # for j in range(EndRowList[ii] - StartRowList[ii] + 1):#每个小问题有EndRowList[ii] - StartRowList[ii] + 1个回答
    #     OneStockQuestionClaimList.append(ClaimData[ClaimNameRow + i + 1][StartRowList[ii]+ j])
    # ClaimSet = list(set(OneStockQuestionClaimList))
    # ClaimSourceMatrix = [['initial'for col in range(1)]for row in range(len(ClaimSet))]
    # for j in range(EndRowList[ii] - StartRowList[ii] + 1):
    #     ClaimSourceMatrix[ClaimSet.index(ClaimData[ClaimNameRow + i + 1][StartRowList[ii]+ j])].append(ClaimData[ClaimNameRow -1][StartRowList[ii]+ j])
    # for j in range(len(ClaimSet)):
    #     ClaimSourceMatrix[j].remove('initial')

    while (1):#repeat
        InterNum += 1
        TempTruthWorthList = copy.deepcopy(TruthWorthList)
        for i in range(len(EndRowList)):#for d ∈ D

            ObserverMatrix = [[0 for col in range(len(SourceNoRepeatMatrix[i]))]for row in range(len(ClaimNoRepeaMatrix[i]))] #|C|行|s|列
            for j in range(EndRowList[i] - StartRowList[i] + 1):
                SourceIndex = SourceNoRepeatMatrix[i].index(ClaimData[ClaimNameRow - 1][StartRowList[i] + j])
                ClaimIndex = ClaimNoRepeaMatrix[i].index(ClaimData[QuestionRow][StartRowList[i] + j])
                ObserverMatrix[ClaimIndex][SourceIndex] = 1
          
            for j in range(len(ClaimNoRepeaMatrix[i])):# for v ∈ Vd
                Pos = 0
                Neg = 0
                for ii in range(len(SourceNoRepeatMatrix[i])):# 遍历Sd
                    if ObserverMatrix[j][ii] == 1: # s ∈ Sv
                        Pos += 1 - TruthWorthList[SourceList.index(SourceNoRepeatMatrix[i][ii])] * ErrorFactorMatrix[i][j]
                    else: # s ∈ S-v
                        Neg += TruthWorthList[SourceList.index(SourceNoRepeatMatrix[i][ii])] * ErrorFactorMatrix[i][j]
                ConfidenceMatrix[i][j] = (Pos + Neg) / len(SourceNoRepeatMatrix[i])
            ConfidenceMatrix[i] = NormalizeList(ConfidenceMatrix[i],Lambda)
            
        for i in range(len(EndRowList)):#for d ∈ D

            ObserverMatrix = [[0 for col in range(len(SourceNoRepeatMatrix[i]))]for row in range(len(ClaimNoRepeaMatrix[i]))] #|C|行|s|列
            for j in range(EndRowList[i] - StartRowList[i] + 1):
                SourceIndex = SourceNoRepeatMatrix[i].index(ClaimData[ClaimNameRow - 1][StartRowList[i] + j])
                ClaimIndex = ClaimNoRepeaMatrix[i].index(ClaimData[QuestionRow][StartRowList[i] + j])
                ObserverMatrix[ClaimIndex][SourceIndex] = 1

            for j in range(len(ClaimNoRepeaMatrix[i])):# for v ∈ Vd
                Norm = 0
                Pos = 0
                Neg = 0
                for ii in range(len(SourceNoRepeatMatrix[i])):# 遍历Sd
                    if TruthWorthList[SourceList.index(SourceNoRepeatMatrix[i][ii])] != 0: # Ts != 0
                        Norm += 1
                        if ObserverMatrix[j][ii] == 1: # s ∈ Sv
                            Pos += (1 - ConfidenceMatrix[i][j]) / TruthWorthList[SourceList.index(SourceNoRepeatMatrix[i][ii])]
                        else:# s ∈ S-v
                            Neg += ConfidenceMatrix[i][j] / TruthWorthList[SourceList.index(SourceNoRepeatMatrix[i][ii])] 
                if Pos + Neg == 0:
                    ErrorFactorMatrix[i][j] == 0.1
                else: 
                    ErrorFactorMatrix[i][j] = (Pos + Neg) / Norm
            ErrorFactorMatrix[i] = NormalizeList(ErrorFactorMatrix[i],Lambda)

        for i in range(len(SourceList)):# for s ∈ S
            Norm = 0
            Pos = 0
            Neg = 0
            s = SourceList[i]
            for j in range(len(EndRowList)):
                if s in SourceNoRepeatMatrix[j]:# d ∈ Ds s对问题d(index = j)做出了声明
                    SourceClaimList = []#是针对问题d的回答list
                    for iii in range(EndRowList[j] - StartRowList[j] + 1 ):
                        if ClaimData[ClaimNameRow - 1][StartRowList[j] + iii] == s:
                            SourceClaimList.append(ClaimData[QuestionRow][StartRowList[j] + iii])
                    for ii in range(len(ClaimNoRepeaMatrix[j])):
                        if ClaimNoRepeaMatrix[j][ii] in SourceClaimList and ErrorFactorMatrix[j][ii] != 0:
                            Pos += (1 - ConfidenceMatrix[j][ii]) / ErrorFactorMatrix[j][ii]
                            Norm += 1
                        else:
                            if ErrorFactorMatrix[j][ii] != 0:
                                Neg += ConfidenceMatrix[j][ii] / ErrorFactorMatrix[j][ii]
            if Norm == 0:
                continue
            TruthWorthList[i] = (Pos + Neg) / Norm
        TruthWorthList = NormalizeList(TruthWorthList,Lambda)

        #检查是否收敛
        v0 = list(map(lambda x: abs(x[0]-x[1]), zip(TruthWorthList, TempTruthWorthList)))
        if max(v0) < yuzhi or InterNum == 100:
            if InterNum == 100:
                print("第",QuestionRow - ClaimNameRow,"个问题无法收敛")
            break
    #结束repeat
    for i in range(len(EndRowList)):
        ThreeEstimatesValueList.append(ClaimNoRepeaMatrix[i][ConfidenceMatrix[i].index(max(ConfidenceMatrix[i]))])  
                
    return ThreeEstimatesValueList

def ThreeEstimates(SourceList,ClaimData,QuestionKindNum,ClaimNameRow,TruthValueMatrixDataStorePath):
    ClaimNameList = []
    #这里的2是为了去除前两行的行标等
    print("3-Estimates is working")
    for i in range(ClaimData.shape[0] - 2):
        if ClaimData[ClaimNameRow][i + 2] not in ClaimNameList:
            ClaimNameList.append(ClaimData[ClaimNameRow][i + 2])
    ThreeEstimatesValueMatrix = [[0 for col in range(QuestionKindNum + 1)]for row in range(len(ClaimNameList))]  
    for i in range(len(ClaimNameList)):
        ThreeEstimatesValueMatrix[i][0] = ClaimNameList[i]    
    for i in range(QuestionKindNum):
        print("Num",i+1,"Question")
        ValueList = CompThreeEstimates(ClaimData,SourceList, i + ClaimNameRow + 1,0.5,ClaimNameRow)
        for j in range(len(ThreeEstimatesValueMatrix)):
            ThreeEstimatesValueMatrix[j][i + 1] = ValueList[j]
    df = pd.DataFrame(ThreeEstimatesValueMatrix)#list不能直接转为excel，需要先转为DataFrame
    df.to_excel(TruthValueMatrixDataStorePath,sheet_name='data1',na_rep='空值')
    print("3-Estimates ends")
    return ThreeEstimatesValueMatrix
if __name__ == '__main__':
    # ClaimData = pd.read_excel(r"C:\SEU\DASI\项目\网络真值\code\Stock\Normalize\WithClaimTruth.xlsx",header= None,keep_default_na=False)
    # ThreeEstimatesValueMatrixDataStorePath = r"C:\SEU\DASI\项目\网络真值\code\CompareA\ThreeEstimates\StockClaim1.xlsx"
    # ThreeEstimates(StockSourceList,ClaimData,16,4,ThreeEstimatesValueMatrixDataStorePath)
    # StockClaim1 = pd.read_excel(r"C:\SEU\DASI\项目\网络真值\code\Stock\Normalize\Data\ClaimNormalize1.xlsx",header= None,keep_default_na=False)
    # StockThreeEstimatesStorePath1 = r"C:\SEU\DASI\项目\网络真值\code\CompareA\ThreeEstimates\Stock1.xlsx"
    # ThreeEstimates(StockSourceList,StockClaim1,1,3,StockThreeEstimatesStorePath1)
    # FlightClaim0 = pd.read_excel(r"C:\SEU\DASI\项目\网络真值\code\FlightData\Normalize\WithTruthClaimNormalize.xlsx",header= None,keep_default_na=False)
    # FlightThreeEstimatesStorePath0 = r"C:\SEU\DASI\项目\网络真值\code\CompareA\ThreeEstimates\Flight0.xlsx"
    # ThreeEstimates(FlightSourceList,FlightClaim0,6,3,FlightThreeEstimatesStorePath0)
    # FlightClaim1 = pd.read_excel(r"C:\SEU\DASI\项目\网络真值\code\FlightData\Normalize\Claim\ClaimNormalize1.xlsx",header= None,keep_default_na=False)
    # FlightThreeEstimatesStorePath1 = r"C:\SEU\DASI\项目\网络真值\code\CompareA\ThreeEstimates\Flight1.xlsx"
    # ThreeEstimates(FlightSourceList,FlightClaim1,6,3,FlightThreeEstimatesStorePath1)
    # start = time.time()
    # BookClaim = pd.read_excel(r"C:\SEU\DASI\项目\网络真值\code\Book\Normalize\ClaimNormalize.xlsx",header= None,keep_default_na=False)
    # ThreeEstimatesBookStorePath = r"C:\SEU\DASI\项目\网络真值\code\CompareA\ThreeEstimates\Book.xlsx"
    # ThreeEstimates(BookSourceList,BookClaim,1,2,ThreeEstimatesBookStorePath)
    # print(time.time() - start)
    # input("xs")

#region stock 5.25
    # ClaimPathList = ["/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize1.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize4.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize5.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize6.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize7.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize8.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize11.xlsx","/home/zhanghe/code_BE/Stock/Normalize/Data/ClaimNormalize12.xlsx"]
    # StorePathList = ["/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value1.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value4.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value5.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value6.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value7.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value8.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value11.xlsx",
    #                  "/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/value12.xlsx"]
    # start = time.time()
    # for i in range(len(ClaimPathList)):
    #     StockClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
    #     ThreeEstimates(StockSourceList,StockClaim,16,3,StorePathList[i])
    # f=open("/home/zhanghe/code/baseline/ThreeEstimates/stock/5.25/time.txt",'w')
    # f.write(str(time.time()-start))
    # f.close
    #endregion
#region flight
    ClaimPathList = ["/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize121.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize122.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize123.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize124.xlsx","/home/zhanghe/code_BE/FlightData/Normalize/Claim/ClaimNormalize125.xlsx"]
    StorePathList = ["/home/zhanghe/code/baseline/ThreeEstimates/flight/5.29/value121.xlsx",
                     "/home/zhanghe/code/baseline/ThreeEstimates/flight/5.29/value122.xlsx",
                     "/home/zhanghe/code/baseline/ThreeEstimates/flight/5.29/value123.xlsx",
                     "/home/zhanghe/code/baseline/ThreeEstimates/flight/5.29/value124.xlsx",
                     "/home/zhanghe/code/baseline/ThreeEstimates/flight/5.29/value125.xlsx"]
    start = time.time()
    for i in range(len(ClaimPathList)):
        FlightClaim = pd.read_excel(ClaimPathList[i],header= None,keep_default_na=False)
        ThreeEstimates(FlightSourceList,FlightClaim,6,3,StorePathList[i])
    f=open("/home/zhanghe/code/baseline/ThreeEstimates/flight/5.29/time.txt",'w')
    f.write(str(time.time()-start))
    f.close
    #endregion