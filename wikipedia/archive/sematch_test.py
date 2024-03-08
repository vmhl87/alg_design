from sematch.semantic.similarity import WordNetSimilarity
wns = WordNetSimilarity()

def similarity(a, b):
	return wns.word_similarity(a, b, 'li')

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

avgFirstOrder, avgSecondOrder = 0, 0

for word in firstOrder:
	avgFirstOrder += similarity(rootWord, word)

avgFirstOrder /= len(firstOrder)

for word in secondOrder:
	avgSecondOrder += similarity(rootWord, word)

avgSecondOrder /= len(secondOrder)

print("Average similarity between words of first order:", avgFirstOrder)
print("Average similarity between words of second order:", avgSecondOrder)
