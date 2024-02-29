import cohere
from cohere.responses.classify import Example
co = cohere.Client('shoQXKOIsvHPwYo86Qfp8zIja2pJ3sCJk9YLwePB')

rootWord = "polar bear"

firstOrder = [
	"bear",
	"arctic",
	"brown bear",
	"carnivore",
	"pagophilic",
	"marine mammals",
	"marine ecosystems",
	"seals",
	"ringed seals",
	"blubber",
	"walruses",
	"beluga whales",
	"maternity dens",
	"vulnerable species",
	"climate change",
	"native",
	"zoos"
]

secondOrder = [
	"species",
	"habitats",
	"North America",
	"South America",
	"Eurasia",
	"plantigrade",
	"giant panda",
	"herbivorous",
	"omnivorous",
	"solitary animals",
	"sense of smell",
	"hibernation",
	"prehistoric",
	"mythology",
	"dance",
	"poaching",
	"polar region",
	"Siberia",
	"Greenland",
	"Arctic Ocean",
	"permafrost",
	"tundra",
	"zooplankton",
	"phytoplankton",
	"subarctic",
	"meat",
	"animal",
	"plant",
	"food",
	"energy",
	"muscle",
	"fat",
	"soft tissues",
	"hunting",
	"scavenging",
	"ice seals",
	"water ice",
	"mammals",
	"cetaceans",
	"whales",
	"dolphins",
	"sirenians",
	"sea otters",
	"molting",
	"habitat degradation",
	"echolocating",
	"gray whale",
	"elephant seal"
	"aquatic",
	"waters",
	"salt",
	"benthic",
	"oceanic",
	"intertidal zone",
	"mudflats",
	"seagrass meadows",
	"mangroves",
	"hydrothermal vents",
	"classes",
	"brown algae",
	"corals",
	"echinoderms",
	"sharks",
	"ocean chemistry",
	"ocean acidification",
	"icebergs",
	"glaciers",
	"calve",
	"ice shelves",
	"density",
	"marine reptiles",
	"plesiosaurs",
	"tusks",
	"whiskers",
	"subterranean",
	"snow caves",
	"fossil fuel use",
	"greenhouse gases",
	"permafrost",
	"radiates",
	"carbon dioxide",
	"Russians",
	"exhibition",
	"conservation",
	"zoology"
]

examples=[
    Example("polar bear", 'root'),
    Example("white bear", 'root'),
    Example("arctic bear", 'root')
]

for i in firstOrder:
    examples.append(Example(i, 'first order'))

for i in secondOrder:
    examples.append(Example(i, 'second order'))

inputs=[
    "salmon",
    "USA census",
    "lion",
    "hunting",
]

response = co.classify(
  inputs=inputs,
  examples=examples,
)

output = response.classifications

for i in output:
    print("The prediction for " + i.input + " is " + i.predictions[0])
