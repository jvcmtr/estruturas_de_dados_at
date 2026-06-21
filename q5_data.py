

DELIVERIES = [ 
  # (Bairro,        t1, t2, priority)
    ("Copacabana",	10, 45,  4),
    ("Ipanema",		25, 75,  5),
    ("Tijuca",		15, 60,  3),
    ("Madureira",	60, 130, 3),
    ("Jacarepagua",	80, 150, 2),
    ("Botafogo",	20, 70,  2)
]

NODES = [ 
  # (Nome,          is_hub)
    ("Centro",		True ), 
    ("Barra",		True ),
    ("Botafogo",	False),
    ("Copacabana",  False),
    ("Ipanema",		False),
    ("Tijuca",		False),
    ("Madureira",	False),
    ("Jacarepagua", False)
]

TRAJETOS = [ 
  # (Origem,        Destino,        t  )
    ( "Centro",		"Botafogo",		18 ),
    ( "Centro",		"Tijuca",		16 ),
    ( "Centro",		"Madureira",	34 ),
    ( "Botafogo",	"Copacabana",	10 ),
    ( "Botafogo",	"Ipanema",		14 ),
    ( "Botafogo",	"Centro",		20 ),
    ( "Copacabana",	"Ipanema",		9  ),
    ( "Copacabana",	"Botafogo",		12 ),
    ( "Copacabana",	"Centro",		28 ),
    ( "Ipanema",	"Copacabana",	10 ),
    ( "Ipanema",	"Botafogo",		16 ),
    ( "Ipanema",	"Barra",		30 ),
    ( "Tijuca",		"Centro",		18 ),
    ( "Tijuca",		"Madureira",	26 ),
    ( "Tijuca",		"Botafogo",		22 ),
    ( "Madureira",	"Tijuca",		30 ),
    ( "Madureira",	"Centro",		35 ),
    ( "Madureira",	"Jacarepagua",	28 ),
    ( "Jacarepagua","Barra",		18 ),
    ( "Jacarepagua","Madureira",	26 ),
    ( "Barra",		"Jacarepagua",	16 ),
    ( "Barra",		"Ipanema",		32 ),
    ( "Barra",		"Centro",		40 )
]