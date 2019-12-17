const service_codes = [
"AA Agriculture AA41",
"AA Agriculture AA91",
"AC Defense Systems AC21",
"AC Defense Systems AC51",
"AC Defense Systems AC61",
"AD Defense - Other AD21",
"AD Defense - Other AD91",
"AE Economic Growth and Productivity AE91",
"AG Energy AG21",
"AG Energy AG41",
"AG Energy AG61",
"AG Energy AG91",
"AH Environmental Protection AH11",
"AH Environmental Protection AH21",
"AH Environmental Protection AH91",
"AJ General Science and Technology AJ11",
"AJ General Science and Technology AJ21",
"AJ General Science and Technology AJ31",
"AJ General Science and Technology AJ41",
"AJ General Science and Technology AJ71",
"AJ General Science and Technology AJ91",
"AK Housing AK11",
"AN Medical AN11",
"AN Medical AN41",
"AP Natural Resources AP21",
"AP Natural Resources AP31",
"AP Natural Resources AP51",
"AR Space AR11",
"AR Space AR21",
"AR Space AR41",
"AR Space AR91",
"AS Transportation - Modal AS21",
"AS Transportation - Modal AS31",
"AS Transportation - Modal AS41",
"AS Transportation - Modal AS91",
"AT Transportation - General AT31",
"AT Transportation - General AT41",
"AT Transportation - General AT61",
"AT Transportation - General AT91",
"AV Mining Activities AV71",
"AZ Other Research and Development AZ11",
"B000 Chemical/Biological Studies and Analyses  B000",
"B002 Animal and fisheries studies B002",
"B100 Air Quality Analyses  B100",
"B101 Environmental Studies Development of Environmental Impact Statements and Assessments  B101",
"B102 Soil Studies  B102",
"B103 Water Quality Studies  B103",
"B109 Other Environmental Studies  B109",
"B200 Geological Studies  B200",
"B201 Geophysical Studies  B201",
"B202 Geotechnical Studies  B202",
"B204 Seismological Studies  B204",
"B206 Energy Studies  B206",
"B208 Housing and Community Development Studies (incl. Urban/Town Planning Studies)  B208",
"B219 Other Engineering Studies  B219",
"B301 Data Analyses (other than scientific)  B301",
"B303 Mathematical/Statistical Analyses  B303",
"B304 Regulatory Studies  B304",
"B308 Accounting/Financial Management Studies  B308",
"B311 Organization/Administrative/Personnel Studies  B311",
"B314 Acquisition Policy/Procedures Studies  B314",
"B329 Other Administrative Support Studies  B329",
"B400 Aeronautic/Space Studies B400",
"B500 Archeological/Paleontological Studies  B500",
"B503 Medical and health studies B503",
"B506 Economic Studies  B506",
"B509 Other Studies and Analyses  B509",
"C111 Administrative and Service Buildings  C111",
"C112 Airfield, Communication and Missile Facilities  C112",
"C113 Educational Buildings  C113",
"C114 Hospital Buildings  C114",
"C115 Industrial Buildings  C115",
"C116 Residential Buildings  C116",
"C117 Warehouse Buildings  C117",
"C118 Research and Development Facilities  C118",
"C119 Other Buildings  C119",
"C121 Conservation and Development  C121",
"C122 Highways, Roads, Streets, Bridges and Railways  C122",
"C123 Electric Power Generation (EPG)  C123",
"C129 Other Non-Building Structures  C129",
"C130 Restoration  C130",
"C211 Architect - Engineer Services (incl. landscaping, interior layout and designing)  C211",
"C212 Engineering Drafting Services  C212",
"C213 A&E Inspection Services  C213",
"C216 Marine Architect and Engineering Services  C216",
"C219 Other Architect and Engineering Services  C219",
"D301 ADP Facility Operation and Maintenance Services  D301",
"D302 OADP Systems Development Services  D302",
"D303 ADP Data Entry Services  D303",
"D304 ADP Telecommunications and Transmission Services D304",
"D307 Automated Information System Design and Integration Services  D307",
"D308 Programming Services  D308",
"D309 Information and Data Broadcasting or Data Distribution Services  D309",
"D311 ADP Data Conversion Services  D311",
"D312 ADP Optical Scanning Services  D312",
"D315 Digitizing Services (Includes cartographic and geographic information)  D315",
"D316 Telecommunications Network Management Services  D316",
"D317 Automated News Services, Data Services, or Other Information Services. Buying data (the electronic equivalent of books, periodicals, newspapers, etc.)  D317",
"D399 Other ADP and Telecommunications Services (incl. data storage on tapes, Compact Disk (CD), etc.  D399",
"E101 Air Quality Support Services  E101",
"E103 Water Quality Support Services  E103",
"E107 Hazardous Substance Analysis  E107",
"E108 Hazardous Substance Removal, Cleanup, and Disposal Services and Operational Support  E108",
"E109 Leaking Underground Storage Tank Support Services  E109",
"E110 Industrial Investigations, Surveys and Technical Support for Multiple Pollutants  E110",
"E111 Oil Spill Response including Cleanup, Removal, Disposal and Operational Support  E111",
"E199 Other Environmental Services  E199",
"F003 Forest Tree Planting Services  F003",
"F006 Crop Services (incl. Seed Collection and Production Services)  F006",
"F008 Tree Breeding Services (incl. ornamental shrub)  F008",
"F010 Other Range/Forest Improvements Services (non-construction)  F010",
"F011 Pesticides /Insecticides Support Services  F011",
"F020 Other Wildlife Management Services  F020",
"F021 Veterinary/Animal Care Services (incl. Livestock Services)  F021",
"F030 Fisheries Resources Management Services   F030",
"F059 Other Natural Resources and Conservation Services  F059",
"G001 Health Care  G001",
"G009 Other Health Services  G009",
"G100 Care of Remains and/or Funeral Services  G100",
"G101 Chaplain Services  G101",
"G102 Recreational Services (incl. Entertainment Services)  G102",
"G103 Social Rehabilitation Services  G103",
"G199 Other Social Services  G199",
"H1 Quality Control Services  H100",
"H2 Equipment and Materials Testing  H200",
"H3 Inspection Services (incl. commercial testing and Laboratory Services, Except Medical/Dental)  H300",
"H9 Other Quality Control, Testing, Inspection and Technical Representative Services  H900",
"JO Maintenance, Repair, Modification, Rebuilding and Installation of Goods/Equipment J019",
"K0 Personal care services (incl. Services such as barber and beauty shop, shoe repairs and tailoring etc.) K000",
"K100 Custodial - Janitorial Services  K100",
"K101 Fire Protection Services  K101",
"K102 Food Services  K102",
"K104 Trash/Garbage Collection Services - Including Portable Sanitation Services  K104",
"K105 Guard Services  K105",
"K106 Insect and Rodent Control Services  K106",
"K107 Landscaping/Groundskeeping Services  K107",
"K108 Laundry and Dry Cleaning Services  K108",
"K111 Carpet Cleaning  K111",
"K112 Interior Plantscaping  K112",
"K113 Snow Removal/Salt Service (also spreading aggregate or other snow meltings material)  K113",
"K114 Waste Treatment and Storage  K114",
"K115 Preparation and Disposal of Excess and Surplus Property  K115",
"K199 Other Custodial and Related Services  K199",
"L004 Other Insurance Services  L004",
"L005 Credit Reporting Services  L005",
"L006 Banking Services  L006",
"L007 Debt Collection Services  L007",
"L099 Other Financial Services  L099",
"M110 Administrative Facilities and Service Buildings  M110",
"M110 Administrative Facilities and Service Buildings  M119",
"M120 Airfield, Communications, and Missile Facilities  M120",
"M170 Warehouse Buildings  M170",
"M180 Research and Development Facilities  M180",
"M180 Research and Development Facilities  M181",
"M190 Other Buildings  M190",
"M240 Utilities  M240",
"M240 Utilities  M242",
"M290 Other Non-Building Facilities  M290",
"R003 Legal Services  R003",
"R004 Certifications and Accreditations for products and institutions other than Educational Institutions  R004",
"R006 Technical Writing Services  R006",
"R007 Systems Engineering Services  R007",
"R008 Engineering and Technical Services (incl. Mechanical, Electrical, Chemical, Electronic Engineering)  R008",
"R009 Accounting Services  R009",
"R010 Auditing Services  R010",
"R012 Patent and Trade Mark Services  R012",
"R013 Real Property Appraisals Services  R013",
"R019 Other Professional Services  R019",
"R101 Expert Witness  R101",
"R102 Weather Reporting/Observation Services  R102",
"R103 Courier and Messenger Services  R103",
"R104 Transcription Services  R104",
"R105 Mailing and Distribution Services (Excluding Post Office Services)  R105",
"R107 Library Services  R107",
"R108 Word Processing/Typing Services  R108",
"R109 Translation and Interpreting Services (Including Sign Language)  R109",
"R113 Data Collection Services  R113",
"R114 Logistics Support Services  R114",
"R115 Contract, Procurement, and Acquisition Support Services  R115",
"R116 Court Reporting Services  R116",
"R117 Paper Shredding Services  R117",
"R118 Real Estate Brokerage Services  R118",
"R119 Industrial Hygienics  R119",
"R121 Program Evaluation Studies  R121",
"R122 Program Management/Support Services  R122",
"R123 Program Review/Development Services  R123",
"R199 Other Administrative and Management Support Services  R199",
"R201 Civilian Personnel Recruitment (inc. Services of Employment Agencies) R201",
"S000 Gas Services  S000",
"S001 Electric Services  S001",
"S002 Telephone and/or Communications Services (incl. Telegraph, Telex and Cablevision Service)  S002",
"S003 Water Services  S003",
"S099 Other Utilities  S099",
"T000 Communications Studies  T000",
"T001 Market Research and Public Opinion Services (Formerly Telephone and Field Interview Services incl. Focus testing, Syndicated and attitude Surveys)  T001",
"T002 Communications Services (incl. exhibit Services)  T002",
"T003 Advertising Services  T003",
"T004 Public Relations Services (incl. Writing Services, Event Planning and Management, Media Relations, Radio and TV Analysis, Press Services)  T004",
"T005 Arts/Graphics Services  T005",
"T006 Cartography Services  T006",
"T007 Charting Services  T007",
"T008 Film Processing Services  T008",
"T009 Film/Video Tape Production Services  T009",
"T011 Photogrammetry Services  T011",
"T012 Aerial Photographic Services  T012",
"T013 General Photographic Services - Still  T013",
"T014 Print/Binding Services  T014",
"T015 Reproduction Services  T015",
"T016 Topography Services  T016",
"T018 Audio/Visual Services  T018",
"T019 Land Surveys, Cadastral Services (non-construction)  T019",
"T099 Other Communication, Photographic, Mapping, Printing and Publication Services  T099",
"U001 Lectures For Training  U001",
"U002 Personnel Testing  U002",
"U003 Reserve Training (Military)  U003",
"U004 Scientific and Management Education  U004",
"U005 Tuition, Registration, and Membership Fees  U005",
"U006 Vocational/Technical  U006",
"U008 Training/Curriculum Development  U008",
"U009 Informatics Training  U009",
"U010 Certifications and Accreditations for Educational Institutions  U010",
"U099 Other Education and Training Services  U099",
"V001 Motor Freight  V001",
"V002 Rail Freight  V002",
"V005 Motor Passenger Service  V005",
"V010 Taxicab Services  V010",
"V100 Vessel Freight  V100",
"V101 Marine Charter for Things  V101",
"V102 Marine Passenger Service  V102",
"V103 Passenger Marine Charter Service  V103",
"V200 Air Freight  V200",
"V201 Air Charter for Things  V201",
"V202 Air Passenger Service  V202",
"V203 Passenger Air Charter Service  V203",
"V204 Specialty air Services including Aerial Fertilization, Spraying and Seeding  V204",
"V401 Other Transportation Travel and Relocation Services  V401",
"V403 Other Vehicle Charter for Transportation of Things  V403",
"V501 Vessel Towing Service  V501",
"V502 Relocation Services  V502",
"V503 Travel Agent Services  V503",
"V505 Warehousing and Storage Services  V505",
"V506 Salvage of Marine Vessels  V506",
"WO Lease or Rental of Equipment  -"
];
