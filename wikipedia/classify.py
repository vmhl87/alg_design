from cohere.responses.classify import Example
from cohere_client import get_client

co = get_client()

sectors = [
        {
            'name': 'Culture and the arts',
            'sub': [
                {
                    'name': 'Culture and Humanities',
                    'examples': [
                        'Classics',
                        'Critical theory',
                        'Cultural anthropology',
                        'Clothing',
                        'Folklore',
                        'Food and drink culture',
                        'Food and drink',
                        'Language',
                        'Literature',
                        'Museology',
                        'Mythology',
                        'Philosophy',
                        'Popular culture',
                        'Science and culture',
                        'Traditions'
                    ]
                },
				{
					'name': 'The arts and Entertainment',
					'examples': [
						'Arts and crafts',
						'Celebrity',
						'Censorship in the arts',
						'Festivals',
						'Humor',
						'Literature',
						'Museums',
						'Parties',
						'Poetry'
					]
				},
				{
					'name': 'Performing arts',
					'examples': [
						'Circuses',
						'Dance',
						'Film',
						'Music',
						'Opera',
						'Storytelling',
						'Theatre'
					]
				},
				{
					'name': 'Visual arts',
					'examples': [
						'Architecture',
						'Comics',
						'Crafts',
						'Design',
						'Drawing',
						'Film Animation',
						'New media art',
						'Painting',
						'Photography',
						'Sculpture'
					]
				},
				{
					'name': 'Games and Toys',
					'examples': [
						'Board games',
						'Card games',
						'Dolls',
						'Puppetry',
						'Puzzles',
						'Role-playing games',
						'Video games'
					]
				},
				{
					'name': 'Sports and Recreation',
					'examples': [
						'Air sports',
						'American football',
						'Association football',
						'Auto racing',
						'Baseball',
						'Basketball',
						'Boating',
						'Boxing',
						'Canoeing',
						'Cricket',
						'Cycling',
						'Exercise',
						'Fishing',
						'Golf',
						'Gymnastics',
						'Hobbies',
						'Horse racing',
						'Ice hockey',
						'Lacrosse',
						'Olympic Games',
						'Rugby league',
						'Rugby union',
						'Sailing',
						'Skiing',
						'Swimming',
						'Tennis',
						'Track and field',
						'Walking trails',
						'Water sports',
						'Whitewater sports'
					]
				},
				{
					'name': 'Mass media',
					'examples': [
						'Broadcasting',
						'Film',
						'Internet',
						'Magazines',
						'Newspapers',
						'Publications',
						'Publishing',
						'Television',
						'Radio'
					]
				}
            ]
        },
        {
            'name': 'Geography and places',
            'sub': [
                {
					'name': 'Geography',
					'examples': [
                        'Earth',
						'World',
						'Bodies of water',
						'Cities',
						'Communities',
						'Continents',
						'Countries',
						'Deserts',
						'Lakes',
						'Landforms',
						'Mountains',
						'Navigation',
						'Oceans',
						'Populated places',
						'Protected areas',
						'Regions',
						'Rivers',
						'Subterranea',
						'Territories',
						'Towns',
						'Villages'
					]
				}
            ]
        },
        {
            'name': 'Health and fitness',
            'sub': [
				{
					'name': 'Self care',
					'examples': [
						'Health promotion',
						'Life extension',
						'Prevention',
						'Sexual health',
						'Sleep',
						'Skin Care'
					]
				},
				{
					'name': 'Nutrition',
					'examples': [
						'Dietary supplements',
						'Dietetics',
                        'Amino acids',
                        'Minerals',
                        'Nootropics',
                        'Phytochemicals',
                        'Vitamins',
						'Nutritional advice pyramids'
					]
				},
				{
					'name': 'Exercise',
					'examples': [
						'Aerobics',
						'Bodyweight exercise (Calisthenics)',
						'Cycling',
						'Exercise equipment',
						'Exercise instructors',
						'Dancing',
						'Exercise physiology',
						'Hiking',
						'Pilates',
						'Running',
						'Sports',
						'Swimming',
						'Tai chi',
						'Walking',
						'Weight training exercises',
						'Yoga'
					]
				},
                {
					'name': 'Human medicine',
					'examples': [
						'Alternative medicine',
						'Cardiology',
						'Endocrinology',
						'Forensic science',
						'Gastroenterology',
						'Human Genetics',
						'Geriatrics',
						'Gerontology',
						'Gynecology',
						'Hematology',
						'Nephrology',
						'Neurology',
						'Obstetrics',
						'Oncology',
						'Ophthalmology',
						'Orthopedic surgical procedures',
						'Pathology',
						'Pediatrics',
						'Psychiatry',
						'Rheumatology',
						'Surgery',
						'Urology'
					]
				},
                {
					'name': 'Dentistry',
					'examples': [
						'Dental hygiene',
						'Orthodontics'
					]
				}
            ]
        },
        {
            'name': 'Human activities',
            'sub': [
                {
					'name': 'Human activities',
					'examples': [
						'Activism',
						'Agriculture',
						'Arts',
						'Aviation',
						'Commemoration',
						'Communication',
						'Crime',
						'Design',
						'Education',
						'Entertainment',
						'Fictional activities',
						'Fishing',
						'Food and drink preparation',
						'Government',
						'Hunting',
						'Industry',
						'Leisure activities',
						'Navigation',
						'Observation',
						'Performing arts',
						'Physical exercise',
						'Planning',
						'Politics',
						'Recreation',
						'Religion',
						'Human spaceflight',
						'Sports',
						'Trade',
						'Transport',
						'Travel',
						'Underwater human activities',
						'Underwater diving',
						'War',
						'Work'
					]
				},
                {
					'name': 'Impact of human activity',
					'examples': [
						'Human impact on the environment',
                        'Climate change',
                        'Nature conservation',
                        'Deforestation',
                        'Environmentalism',
                        'Global warming',
                        'Pollution',
						'Human overpopulation',
						'Urbanization'
					]
				}
            ]
        },
        {
            'name': 'Mathematics and logic',
            'sub': [
                {
					'name': 'Mathematics',
					'examples': [
						'Mathematics education',
						'Equations',
						'Heuristics',
						'Measurement',
						'Numbers',
						'Proofs',
						'Theorems'
					]
				},
                {
					'name': 'Fields of mathematics',
					'examples': [
						'Arithmetic',
						'Algebra',
						'Geometry',
						'Trigonometry',
						'Mathematical analysis',
						'Calculus'
					]
				},
                {
					'name': 'Logic',
					'examples': [
						'Deductive reasoning',
						'Inductive reasoning',
						'History of logic',
						'Fallacies',
						'Metalogic',
						'Philosophy of logic'
					]
				},
                {
					'name': 'Mathematical sciences',
					'examples': [
						'Computational science',
						'Operations research',
						'Theoretical physics'
					]
				},
                {
					'name': 'Statistics',
					'examples': [
						'Analysis of variance',
						'Bayesian statistics',
						'Categorical data',
						'Covariance and correlation',
						'Data analysis',
						'Decision theory',
						'Design of experiments',
						'Logic and statistics',
						'Multivariate statistics',
						'Non-parametric statistics',
						'Parametric statistics',
						'Regression analysis',
						'Sampling',
						'Statistical theory',
						'Stochastic processes',
						'Summary statistics',
						'Survival analysis',
						'Time series'
					]
				}
            ]
        },
        {
            'name': 'Natural and physical sciences',
            'sub': [
                {
					'name': 'Biology',
					'examples': [
						'Botany',
						'Ecology',
						'Health sciences',
						'Medicine',
						'Neuroscience',
						'Zoology'
					]
				},
                {
					'name': 'Earth sciences',
					'examples': [
						'Atmospheric sciences',
						'Geography',
						'Geology',
						'Geophysics',
						'Oceanography'
					]
				},
                {
					'name': 'Nature',
					'examples': [
						'Animals',
						'Environment',
						'Humans',
						'Life',
						'Natural resources',
						'Plants',
						'Pollution'
					]
				},
                {
					'name': 'Physical sciences',
					'examples': [
						'Astronomy',
						'Chemistry',
						'Climate',
						'Physics',
						'Space',
						'Universe'
					]
				}
            ]
        },
        {
            'name': 'People and self',
            'sub': [
                {
					'name': 'People',
					'examples': [
						'Beginners and newcomers',
						'Children',
						'Heads of state',
						'Humans',
						'People by legal status',
						'Political people',
						'Rivalry',
						'Social groups',
						'Subcultures',
                        'People by city',
						'ethnicity',
						'descent',
						'nationality',
						'occupation',
						'Writers'
					]
				},
                {
					'name': 'Self',
					'examples': [
						'Alter egos',
						'Consciousness',
						'Gender',
						'Personality',
						'Sexuality',
						'Sexual orientation'
					]
				},
                {
					'name': 'Personal life',
					'examples': [
						'Clothing',
						'Employment',
						'Entertainment',
						'Food and drink',
						'Games',
						'Health',
						'Hobbies',
						'Home',
						'Income',
						'Interpersonal relationships',
						'Leisure',
						'Love',
						'Motivation',
						'Personal development',
						'Pets'
					]
				}
            ]
        },
        {
            'name': 'Philosophy and thinking',
            'sub': [
                {
					'name': 'Philosophy',
					'examples': [
						'Branches',
						'Schools and traditions',
						'Concepts',
						'Theories',
						'Arguments',
						'Philosophers',
						'Literature',
						'History',
						'By period',
						'By region',
						'Aesthetics',
						'Epistemology',
						'Ethics',
						'Logic',
						'Metaphysics',
						'Social philosophy'
					]
				},
                {
					'name': 'Thinking / Thinking skills',
					'examples': [
						'Attention',
						'Cognition',
						'Cognitive biases',
						'Creativity',
						'Decision theory',
						'Emotion',
						'Error',
						'Imagination',
						'Intelligence',
						'Learning',
                        'biases',
                        'mnemonics',
						'Nootropics (smart drugs)',
						'Organizational thinking (strategic management)',
						'Perception',
						'Problem solving',
						'Psychological adjustment',
						'Psychometrics'
					]
				}
            ]
        },
        {
            'name': 'Society and social sciences',
            'sub': [
                {
					'name': 'Society',
					'examples': [
						'Activism',
						'Business',
						'Communication',
						'Crime',
						'Education',
						'Ethnic groups',
						'Family',
						'Finance',
						'Globalization',
						'Government',
						'Health',
						'Home',
						'Industries',
						'Infrastructure',
						'Law',
						'Mass media',
						'Military',
						'Money',
						'Organizations',
						'Peace',
						'Politics',
						'Real estate',
						'Rights',
						'War'
					]
				},
                {
					'name': 'Social sciences',
					'examples': [
						'Anthropology',
						'Archaeology',
						'Cultural studies',
						'Demographics',
						'Economics',
						'Information science',
						'International relations',
						'Linguistics',
						'Media studies',
						'Political science',
						'Psychology',
						'Public administration',
						'Sexology',
						'Social scientists',
						'Sociology',
						'Social work',
						'Systems theory'
					]
				}
            ]
        },
        {
            'name': 'Technology and applied sciences',
            'sub': [
                {
					'name': 'Technology',
					'examples': [
                        'Agriculture',
						'Agronomy',
						'Architecture',
						'Automation',
						'Biotechnology',
						'Cartography',
						'Chemical engineering',
                        'Telecommunications',
						'Construction',
						'Control theory',
						'Design',
						'Digital divide',
						'Earthquake engineering',
						'Energy',
						'Ergonomics',
						'Firefighting',
						'Fire prevention',
						'Forensic science',
						'Forestry',
						'Industry',
						'Information science',
						'Internet',
						'Management',
						'Manufacturing',
						'Marketing',
						'Medicine',
						'Metalworking',
						'Microtechnology',
						'Military science',
						'Mining',
						'Nanotechnology',
						'Nuclear technology',
						'Optics',
						'Plumbing',
						'Robotics',
						'Sound technology',
						'Technology forecasting',
						'Tools'
					]
				},
                {
					'name': 'Computing',
					'examples': [
						'Apps',
						'Artificial intelligence',
						'Classes of computers',
						'Companies',
						'Computer architecture',
						'Computer model',
						'Computer engineering',
						'Computer science',
						'Computer security',
						'Computing and society',
						'Data',
						'Embedded systems',
						'Free software',
						'Human–computer interaction',
						'Information systems',
						'Information technology',
						'Internet',
						'Mobile web',
						'Languages',
						'Multimedia',
						'Networks (Industrial)',
						'Operating systems',
						'Platforms',
						'Product lifecycle management',
						'Programming',
						'Real-time computing',
						'Software',
						'Software engineering',
						'Unsolved problems in computer science'
					]
				},
                {
					'name': 'Electronics',
					'examples': [
						'Avionics',
						'Circuits',
						'Companies',
						'Connectors',
						'Consumer electronics',
						'Digital electronics',
						'Digital media',
						'Electrical components',
						'Electronic design',
						'Electronics manufacturing',
						'Embedded systems',
						'Integrated circuits',
						'Microwave technology',
						'Molecular electronics',
						'Water technology',
						'Optoelectronics',
						'Quantum electronics',
						'Radio-frequency identification RFID',
						'Radio electronics',
						'Semiconductors',
						'Signal cables',
						'Surveillance',
						'Telecommunications'
					]
				},
                {
					'name': 'Engineering',
					'examples': [
						'Aerospace engineering',
						'Bioengineering',
						'Chemical engineering',
						'Civil engineering',
						'Electrical engineering',
						'Environmental engineering',
						'Materials science',
						'Mechanical engineering',
						'Nuclear technology',
						'Software engineering',
						'Structural engineering',
						'Systems engineering'
					]
				},
                {
					'name': 'Transport',
					'examples': [
						'By country',
						'Aviation',
						'Cars',
						'Cycling',
						'Public transport',
						'Rail transport',
						'Road transport',
						'Shipping',
						'Spaceflight',
						'Vehicles',
						'Water transport'
					]
				}
            ]
        }
    ]

processed_sectors = []

for sector in sectors:
    for subsector in sector['sub']:
        for example in subsector['examples']:
            processed_sectors.append(
                    Example(example, sector['name'] + ' > ' + subsector['name'])
                )
def project_searchspace(pages):
    response = co.classify(
            inputs=pages,
            examples=processed_sectors,
            model='embed-english-light-v2.0'
        )

    for item in response:
        print(item.input + ' is classified as ' + str(item.predictions))
