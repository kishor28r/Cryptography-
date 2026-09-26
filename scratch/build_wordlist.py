import os

# Base words covering comprehensive English vocabulary
base_text = """
a abandon ability able aboard about above abroad absence absolute absolutely absorb abuse academic accept access
accident accompany accomplish according account accuracy accurate accuse achieve achievement acid acknowledge acquire across
act action active activist activity actor actress actual actually ad adapt add addition additional
address adequate adjust adjustment administration administrator admire admit adopt adult advance advanced advantage
adventure advertising advice advise advocate affair affect afford afraid african after afternoon again
against age agency agenda agent aggressive ago agree agreement agricultural ah ahead aid aide
aim air aircraft airline airport album alcohol alive all alliance allow ally almost alone
along already also alter alternative although always am amazing american among amount analysis analyst
analyze ancient and anger angle angry animal anniversary announce announcement annual another answer anticipate
anxiety anxious any anybody anyone anything anyway anywhere apart apartment apparent apparently appeal appear
appearance apple application apply appoint appointment appreciate approach appropriate approval approve approximately arab
architect architecture area argue argument arise arm armed armor army around arrange arrangement arrest arrival
arrive art article artist artistic as asian aside ask asleep aspect assert assessment asset
assign assignment assist assistance assistant associate association assume assumption assure at athlete athletic atmosphere
attach attack attempt attend attention attitude attorney attract attraction attractive attribute audience aunt author
authority auto available avenue average avoid award aware awareness away awful baby back background
backwards bacon bad badly bag bake balance ball ban banana band bank bar barely barn
barrel barrier base baseball basic basically basis basket basketball bath bathroom battery battle bay be
beach beam bean bear beard beast beat beautiful beauty because become bed bedroom bee beef beer
before beg begin beginner beginning behalf behave behavior behind being belief believe bell belong below
belt bench bend beneath benefit beside besides best bet better between beyond bicycle big bike
bill billion bind bird birth birthday bishop bit bite bitter black blade blame blank blanket
blast bleed blend bless blind blink block blonde blood bloody blow blue board boat body
boil bold bolt bomb bond bone bonus book boom boot border bore bored boring born
borrow boss both bother bottle bottom bound boundary bow bowl box boy brain branch brand
brave bread break breakfast breast breath breathe brick bride bridge brief briefly bright brilliant bring
broad broadcast brother brown brush bubble bucket budget buffer bug build builder building bulb bulk
bullet bunch burden burn burst bus bush business busy but butter button buy buyer by
cabin cabinet cable cage cake calculate calculation calendar call calm camera camp campaign campus can
canal cancel cancer candidate candle candy canvas cap capability capable capacity capital captain capture car
card care career careful carefully careless cargo carpet carriage carrier carrot carry cart case cash
cast castle casual cat catch category cattle cause caution cautious cave ceiling celebrate celebration cell
cellar cement cemetery center central century cereal certain certainly chain chair chairman challenge chamber champion
championship chance change channel chaos chapter character characteristic characterize charge charity charm charming chart
chase cheap check cheek cheer cheese chef chemical chemistry cheque cherry chest chew chicken
chief child childhood children chill chimney chin china chip choice choir choose chop chorus
chronic church cigarette cinema circle circuit circulate circulation circumstance cite citizen city civil civilian
claim clash class classic classical classification classify classroom clay clean cleaner clear clearly
clerk clever click client cliff climate climb cling clinic clock close closely closet cloth clothes
clothing cloud cloudy club clue cluster coach coal coast coat code coffee coin cold collapse
collar colleague collect collection collective collector college colony color column columnar combat combination combine
come comedy comfort comfortable comic command commander commence comment commercial commission commit commitment committee
common commonly communicate communication community companion company compare comparison compass compel compensate compensation compete
competition competitive competitor compile complaint complete completely completion complex complexity compliance complicate complicated component
compose composition compound comprehensive comprise compute computer comrade conceal concede concept conception concern concerned
conclude conclusion concrete condemn condition conduct conductor confer conference confess confession confidence confident confirm
confirmation conflict conform confront confrontation confusion congratulate congress connect connection conquer conscience conscious consciousness
consent consequence consequently conservation conservative consider considerable considerably consideration consist consistent consistently console consolidate
constitute constitution constitutional constrain constraint construct construction consult consultant consume consumer consumption contact contain
container contemporary contend content context continent continue continued continuous contract contrast contribute contribution
contributor control controversial controversy convention conventional conversation conversion convert convey convict conviction convince
convincing cook cooker cookie cooking cool cooperate cooperation cope copper copy core corn corner
corporate corporation correct correctly correlate correlation correspond correspondence correspondent corridor cost costly cottage cotton
couch council counsel counselor count counter counterattack counterfeit country countryside county couple courage course
court cousin cover coverage cow crack craft crash crawl crazy cream create creation creative
creativity creator creature credit creditcard crew crime criminal crisis crisp criterion critic critical criticism
criticism criticize crop cross crowd crowded crown crucial crude cruel cruise crush cry crystal
cube cult cultural culture cup cupboard cure curious currency current currently curriculum curtain curve
casing custom customer customhouse cut cycle dad daily dairy dam damage dame damn dance
dancer dancing danger dangerous dare dark darkness data date daughter dawn day daylight dead
deadline deadly deaf deal dealer dear death debate debt decade decay deceit decent decide
decision deck declare decline decorate decoration decorative decrease deduce deed deep deeply deer defeat
defect defence defend defender defense deficit define definite definitely definition degree delay deliberate deliberately
delicate delight delighted delightful deliver delivery demand democracy democrat democratic demonstrate demonstration denial dense
density deny depart department departure depend dependent depending depict deploy deposit depress depressed depressing
depression depth deputy derive descend descendant descent describe description desert deserve design designer desire
desk desperate desperately despite dessert destroy destruction detail detailed detect detective determination determine
determined develop developer development device devil devote devoted diagram dial dialect dialogue diamond diary
dictator dictionary die diet differ difference different differential differently difficult difficulty dig digest digital
dignity dilemma dimension diminish dinner dip diploma diplomacy diplomat diplomatic direct direction directly director
directory dirt dirty disability disable disadvantage disagree disagreement disappear disappoint disappointed disappointment disaster disc
discard discharge discipline disclose disclosure discount discourage discover discovery discuss discussion disease dish dishonest
disk dislike dismiss disorder dispatch display disposal dispose dispute disrupt dissatisfaction dissolve distance distant
distinct distinction distinctive distinguish distract distress distribute distribution district disturb disturbance ditch dive diverse
diversity divide dividend divine division divorce doctor document documentary dog dollar domain domestic dominant
dominate door door-to-door dose dot double doubt doubtfully doubtfully dough down download downhill downright
draft drag dragon drain drama dramatic dramatically draw drawer drawing dream dress drift drill
drink drive driver drop drown drug drum drunk dry duck due dull dumb dump
during dust duty dwarf dwell dying dynamic eager eagle ear early earn earnest earth
ease easily east eastern easy eat echo economic economical economics economist economy edge edit
edition editor educate educated education educational educator effect effective effectively efficiency efficient effort egg
eight eighteen eighty either elbow elder elderly elect election elector electric electrical electrician electricity
electron electronic electronics elegant element elementary elephant elevate elevation eleven eliminate elite else elsewhere
embarrass embarrassed embarrassing embarrassment embassy emerge emergency emission emotion emotional emotionally emphasis emphasize empire
employ employee employer employment empty enable enclose encounter encourage encouragement end endanger endeavor ending
endless endorse endorsement endure enemy energy enforce engagement engine engineer engineering english enjoy enjoyable
enormous enough enquire enquiry ensure enter enterprise entertain entertainment enthusiasm enthusiastic entire entirely entitle
entrance entry envelope environment environmental envy episode equal equality equally equation equip equipment equivalent
era erase error escape especially essay essence essential essentially establish establishment estate estimate eternal
ethnic european evaluate evaluation even evening event eventually ever every everybody everyday everyone everything
everywhere evidence evident evil exact exactly exaggerate examination examine example exceed excellence excellent except
exception exceptional excess excessive exchange excite excited excitement exciting exclude exclusion exclusive exclusively excuse
execute execution executive exercise exhaust exhausted exhibit exhibition exist existence exit exotic expand expansion
expect expectation expected expend expenditure expense expensive experience experienced experiment experimental expert expertise
explain explanation explicit explicitly explode exploit exploitation exploration explore explosion explosive export expose exposure
express expression extend extension extensive extent external extra extract extraordinary extreme extremely eye eyebrow
eyelashes eyelid face facility fact factor factory faculty fade fail failure faint fair
fairly faith faithful fake fall false fame familiar family famous fan fancy fantastic
far fare farm farmer farming fascinate fascinating fashion fashionable fast fasten fat fatal
fate father fatigue fault faulty favor favorable favorite fear fearful feasible feast feather
feature february federal fee feed feedback feel feeling fellow female fence ferry festival
fetch fever few fiber fiction field fierce fifteen fifth fifty fight fighter fighting figure
file fill film filter final finally finance financial find finding fine finger finish
fire firearm fireplace firm firmly first fish fisherman fishing fit fitness five fix
flag flame flash flat flavor flee fleet flesh flexible flight float flood floor
flour flourish flow flower flu fluid fly flying foam focus fog fold folk
follow follower following food fool foolish foot football for forbid force forecast foreign
foreigner forest forever forge forget forgive fork form formal format formation former formerly
formula forth fortnight fortunate fortunately fortune forty forward fossil foster found foundation founder
fountain four fourteen fourth fox frame framework franc France free freedom freeze freezer
freight french frequency frequent frequently fresh Friday fridge friend friendly friendship fright frighten
frightened frightening frog from front frontier frost frown fruit frustrate frustration fry fuel
full fully fun function fund fundamental funeral funny fur furnace furnish furniture further
furthermore future gain gallery gamble gambling game gang gap garage garden gardener garlic
gas gasoline gate gather gauge gear general generally generate generation generator generous genius
gentle gentleman genuine geography gesture get ghost giant gift gifted giraffe girl give
given glad glance glass globe gloomy glorious glory glove glow glue go goal
goat god gold golden golf good goodbye goodness goods goose govern government governor
grace graceful grade gradual gradually graduate grain grammar grand grandchild granddad granddaughter grandfather
grandmother grandparent grandson grant grape graph grasp grass grateful grave gravity gray great
greatly greed greedy green greenhouse greet greeting grief grief-stricken grill grim grin grind
grip grocery ground group grow growth guarantee guard guess guest guidance guide guilt
guilty guitar gun guy habit habitat hair haircut half hall halt hammer hand
handbook handful handkerchief handle handsome handy hang happen happily happiness happy harbor hard
hardly hardship hardware harm harmful harmless harmony harsh harvest hat hate hatred have
hay hazard he head headache headline headmaster headquarters heal health healthy heap hear
hearing heart heat heater heating heaven heavily heavy heel height helicopter hell hello
helmet help helpful helpless hen hence her herb herd here hero heroic herself
hesitate hesitation hi hide high highlight highly highway hill him himself hint hire
his historian historic historical history hit hobby hold holder hole holiday hollow holy
home homeland homeless honest honesty honey honor honorable hook hope hopeful hopeless horizon
horizontal horn horrible horror horse hospital host hostage hostile hot hotel hour house
household housewife housing how however huge human humanity humble humor humorous hundred hunger
hungry hunt hunter hurricane hurry hurt husband hut hypothesis I ice icy idea
ideal identical identify identity ideological ideology idiot idle if ignore ill illegal illness
illusion illustrate illustration image imaginary imagination imagine immediate immediately immense immigrant impact impatient
imperial implement implication imply import importance important impose impossible impress impression impressive improve
improvement impulse in incentive incident incline include including income incorporate increase increasingly incredible
incredibly indeed independence independent index indicate indication individual indoor indoors industrial industry inevitable
inevitably infant infect infection infectious infer infernal infinite inflation influence influential inform informal
information ingredient inhabitant initial initially initiative inject injection injure injured injury ink inn
inner innocent innovation input inquiry insane insect inside insight insist inspection inspector inspiration
inspire install instance instant instantly instead instinct institute institution instruct instruction instructor instrument
insult insurance intact integral integrate integration integrity intellect intellectual intelligence intelligent intend intense
intensity intensive intention interact interaction interest interested interesting interface interfere interference interior intermediate
internal international internet interpret interpretation interrupt interval intervene intervention interview intimate into introduce
introduction invade invader invasion invent invention inventory invest investigate investigation investigator investment investor
invisible invitation invite involve involved involvement inward iron irony island isolate isolated issue
it italian item its itself jacket jail jam january jar jaw jazz jealous
jealousy jeans jet jewel jewelry job join joint joke journal journalist journey joy
judge judgment judicial jug juice july jump junction june jungle junior jury just
justice justification justify keen keep key keyboard kick kid kill killer kilogram kilometer
kind kindness king kingdom kiss kitchen knee kneel knife knight knock knot know
knowledge lab label labor laboratory lack ladder lady lake lamb lamp land landlord
landscape lane language lap large largely laser last late lately later latest latter
laugh laughter launch laundry law lawn lawyer lay layer lead leader leadership leading
leaf league leak lean leap learn learned learning least leather leave lecture lecturer
left leg legal legend legislation legislative legislator legislature legitimate leisure lemon lend length
lens less lesson let letter level liberal liberty library license lid lie life
lifestyle lifetime lift light lighter lighting lightning like likelihood likely limb limit limitation
limited line linear line-up linen linger link lion lip liquid list listen listener
literary literature little live lively liver living load loan lobby local locate location
lock log logic logical lonely long look loop loose lord lose loss lost
lot lottery loud loudly love lovely lover low lower loyal loyalty luck lucky
luggages lump lunch lung luxury machine machinery mad madam magazine magic magical magician
magnet magnetic magnificent maid mail main mainland mainly mainstream maintain maintenance major majority
make maker makeup male malice mall man manage management manager mankind manner manual
manufacture manufacturer manufacturing many map march margin marine mark market marketing marketplace marriage
married marry marvelous mask mass massive master masterpiece match matching material mathematical mathematics
matrix matter maximum may maybe mayor me meadow meal mean meaning means meantime
meanwhile measure measurement meat mechanic mechanical mechanism medal media medical medication medicine medium
meet meeting melody melt member membership memory mental mention menu merchant mercy mere
merely merit mess message metal metallic meter method metric microphone microprocessor middle midnight
midst might migrate mild mile military milk mill millimeter million mind mine miner
mineral minimum minister ministry minor minority minute miracle mirror miserable misery miss missile
missing mission mistake mistaken mix mixture mob mobile mode model moderate modern modest
modest moment momentum monday money monitor monk monkey month monthly monument mood moon
moral morality more moreover morning mortgage mosquito most mostly mother motion motivate motivation
motive motor mount mountain mounted mouse mouth move movement movie much mud multiple
multiply murder murderer muscle museum music musical musician must mustard mutter mutual my
myself mysterious mystery myth nail naked name napkin narrow nation national nationality native
natural naturally nature navy near nearby nearly neat necessarily necessary neck need needle
negative neglect negotiate negotiation neighbor neighborhood neighborly neither nephew nerve nervous nest
net network neutral never nevertheless new news newspaper next nice niece night nightmare
nine nineteen ninety no noble nobody noise noisy nominate nomination non none nonetheless
nonsense noon nor norm normal normally north northern nose not notable note notebook
nothing notice noticeable notify notion noun novel novelist november now nowhere nuclear number
numerous nurse nursery nut nutrition nylon oak obediant obey object objection objective obligation
observation observe observer obstacle obtain obvious obviously occasion occasional occasionally occupation occupy occur
ocean o'clock october odd odds of off offense offensive offer office officer official
often oil old olive Olympic omission omit on once one oneself onion online
only onset onward open opening opera operate operation operational operator opinion opponent opportunity
oppose opposed opposite opposition option optional or orange orbit orchestra order ordinary organ
organic organization organize organized organizer origin original originally ornament other otherwise ought our
ours ourselves out outcome outdoor outdoors outer outline output outrage outside outstanding oven
over overall overcome overlook overnight overseas owe owl own owner ox oxygen pace
pack package packet pad page pain painful paint painter painting pair palace pale
palm pan panel panic paper parade paradise paragraph parallel parcel pardon parent park
parliament part partial partially participant participate participation particular particularly partly partner partnership party
pass passage passenger passing passion passive passport past pastry path patience patient patrol
pattern pause paw pay payment peace peaceful peach peak pear peasant pebble peculiar
pedal peel peep peer pen penalty pencil penguin penny pension people pepper per
perceive percent percentage perception perfect perfectly perform performance performer perfume perhaps period permanent
permission permit person personal personality personally personnel perspective persuade pest pet petrol petroleum
phase philosopher philosophy phone photo photograph photographer photography phrase physical physician physicist physics piano
pick picnic picture pie piece pierce pig pigeon pile pill pillar pillow pilot
pin pinch pine pink pint pipe pirate pit pitch pity place plain plan
plane planet plank planner plant plastic plate platform play player playful playground plea
pleasant please pleased pleasure pledge plentiful plenty plight plot plow plug plum plunge
plus pocket poem poet poetry point poison poisonous poke pole police policeman policy
polish polite political politician politics poll pollution pond pool poor pop popular population
porcelain pork port portion portrait portray pose position positive possess possession possibility possible
possibly post postage postal poster pot potato potential potter pouch poultry pound pour
poverty powder power powerful practical practice praise pray prayer preach precaution precedent precious
precise precisely predict prediction prefer preference prefix pregnant prejudice preliminary premise premium preparation
prepare prescription presence present presentation preserve president press pressure prestige presumably presume pretend
pretty prevail prevent prevention previous previously price prick pride priest primary prime primitive
prince princess principal principle print printer prior priority prison prisoner privacy private privilege
prize probability probable probably problem procedure proceed process produce producer product production profession
professional professor profile profit program progress progressive project prominent promise promote prompt proof
proper properly property proportion proposal propose prosecution prospect protect protection protective protein protest
proud prove provide provided provider province provision provoke psychological psychologist psychology public publication
publicity publish publisher puddle pull pulse pump punch punish punishment pupil purchase pure
purple purpose purse pursue push put puzzle qualification qualify quality quantity quarrel quarter
queen quench quest question queue quick quickly quiet quietly quilt quit quite quiver
quote rabbit race racial racing rack radar radiator radical radio radius rage raid
rail railroad railway rain rainbow raise rake rally ramp ranch random range rank
rapid rapidly rare rarely rascal rat rate rather rating ratio rational raw ray
reach react reaction read reader readily reading ready real realistic reality realize really
realm reap rear reason reasonable reassure rebel rebellion recall receipt receive recent recently
reception receptionist recipe recipient reckon reclaim recognition recognize recommend recommendation reconstruct record recorder
recording recover recovery recruit rectangle red reduce reduction reed refer reference refine reflect
reflection reform refrigerator refuge refugee refusal refuse regain regard regarding regardless regime region
regional register regret regular regularly regulate regulation regulator rehearsal reign reinforce reject rejoice
relate relation relationship relative relatively relax relaxation relay release relent relevant reliable reliance
relief religion religious reload rely remain remainder remaining remark remarkable remedy remember remind
remicence remnant remote removal remove render renew rent repair repay repeat repeated repeatedly
replace replacement reply report reporter represent representation representative republic republican reputation request require
requirement rescue research researcher resemblance resent resentment reservation reserve reservoir reside resident residential
resign resignation resist resistance resolution resolve resort resource respect respective respectful respond respondent
response responsibility responsible rest restaurant restore restrain restraint restrict restriction result resume retail
retain retire retirement retreat return reveal revenge revenue reverse review revise revision revival revive
revolting revolution revolutionary revolve reward rhetoric rhythm rib ribbon rice rich rid ride
rider ridge ridicule ridiculous rifle right rigid ring riot rip ripe rise risk
rival river road roar roast rob robber robbery robot robust rock rocket rod
roll roller romance romantic roof room root rope rose rot rotate rotation rough
roughly round route routine row royal rub rubber rubbish ruby rude ruin rule
ruler rumor run runner running rural rush rust sacred sad saddle safe safety
sail sailor saint sake salad salary sale salesman salmon salt same sample sand
sandwich sane sanitary satellite satisfaction satisfactory satisfy sauce saucepan saucer sausage savage save
savings saw say scale scandal scan scar scarce scarcely scare scared scarf scatter
scene scenery scent schedule scheme scholar scholarship school science scientific scientist scissors scold
scoop scope score scorn scorpion scout scramble scrap scrape scratch scream screen screw
script sculpture sea seal seam search season seat second secondary secret secretary section
sector secure security see seed seek seem segment seize select selection self selfish
sell seller semester seminar senate senator send senior sensation sense sensible sensitive sentence
sentiment sentimental separate separation september sequence serene series serious seriously servant serve service
session set setting settle settlement settler seven seventeen seventy several severe severely sew
sewer sex sexual shadow shady shake shall shallow shame shampoo shape share shark
sharp shatter shave she shed sheep sheet shelf shell shelter shepherd shield shift
shine shiny ship shipment shirt shock shoe shoot shop shore short shortage shortcoming
shortly shot should shoulder shout shove show shower shred shrewd shriek shrimp
shrine shrink shrub shrug shudder shuffle shut shy sibling sick sickness side sidewalk
siege sigh sight sign signal signature significance significant signify silence silent silk silly
silver similar similarity simple simplify simply sin since sincere sincerity sing singer single
sink sir siren sister sit site situation six sixteen sixty size skate skeleton
sketch skill skilled skin skip skirt skull sky slap slate slave sleep slender
slice slide slight slightly slim slip slipper slippery slope slot slow slowly slug
smack small smart smash smell smile smoke smooth smother smuggle snack snail snake
snap snare snatch sneak sneeze sniff snow soak soap soar soccer social society
sock socket sofa soft soften software soil solar solder soldier sole solely solemn
solid solitary solitude solution solve somber some somebody somehow someone something sometimes somewhat
somewhere son song soon soot sore sorrow sorry sort soul sound soup sour
source south southern souvenir sovereign sow space spade span spanish spare spark sparkle
sparrow speak speaker spear special specialist specialty species specific specify specimen spectacle spectator
spectrum speech speed spell spelling spend sphere spice spider spill spin spine spirit
spiritual spit spite splash splendid split spoil spoke spokesman sponge sponsor spoon sport
spot spouse spout spread spring sprinkle spur spy squad square squash squeeze squirrel
stable stadium staff stage stain stair staircase stake stale stall stamp stand standard
standing star stare start startle state statement station statistics statue status stay steady
steak steal steam steel steep steer stem step sterile stick stiff stifle still
stimulate sting stink stir stitch stock stocking stomach stone stool stoop stop
storage store storm story stout stove straight strain strait strand strange stranger strap
strategy straw stray stream street strength strengthen stress stretch strict strictly stride strike
string strip stripe strive stroke strong structural structure struggle stubborn student studio study
stuff stumble stump stupid sturdy style subject submarine submit submerge subscribe subsequent substance
substantial substitute subtle subtract suburb suburban succeed success successful succession successive successor such
suck sudden suddenly suffer suffering sufficient suffix sugar suggest suggestion suicide suit suitable
suitcase suite suitor sulfure sum summary summer summit summon sun sunday sunflower sunlight
sunny sunrise sunset sunshine super superb superior supermarket supervise supervisor supper supplement supply
support supporter suppose supreme sure surface surge surgeon surgery surprise surrender surround survey
survival survive survivor suspect suspend suspense suspicion suspicious sustain swallow swamp swan swear
sweat sweep sweet swell swift swim swing switch sword syllable symbol sympathy symphony
symptom synonym synthetic syrup system table tablet tackle tag tail tailor take tale
talent talk tall tame tan tank tap tape target tariff task taste tax
taxi tea teach teacher team tear tease technical technique technology teen teenager telegram
telephone telescope television tell temper temperature tempest temple temporary tempt tenant tend tendency
tender tennis tense tension tent term terminal terminate terrible terrific terrify territory terror
test testament testify testimony testing text textbook than thank thanks that thaw the
theater theatre theft their them theme themselves then theoretical theory therapy there thereby
therefore thermometer these thesis they thick thief thigh thin thing think third thirst
thirty this thorn thorough those though thought thousand thread threat threaten three threshold
thrill thrive throat throne throng through throw thrust thumb thunder thursday thus tick
ticket tide tidy tie tiger tight tile timber time timid tin tiny tip
tire tissue title to toad toast tobacco today toe together toilet token told
tolerable tolerate toll tomato tomb tomorrow tone tongue tonight too tool tooth top
topic torch torment tornado torrent tortoise toss total totally touch tough tour tourist
tournament toward towel tower town toy trace track tractor trade trademark trader tradition
traffic tragedy tragic trail train traitor tramp trample trance transaction transfer transform translate
translation transmission transmit transport transportation trap trash travel traveler tray treachery tread treason
treasure treasury treat treatment treaty tree tremble tremendous trench trend trial triangle tribe
trick trickle trifle trigger trim trio trip triumph troop trophy tropical trouble trough
trousers trout truck true truly trumpet trunk trust truth try tub tube
tug tuition tulip tumble tune tunnel turbine turf turkey turn turnip turnover tutor
twelve twenty twice twig twin twist two type typical typist ugly ultimate umbrella
umpire unable uncle unawares uncertain uncle uncleanness unconscious under undergo underground underline understand
undertake undo undoubtedly undress uneasy unemployed unexpected unfair unfit unfold unfortunate ungrateful
unhappy uniform union unique unit unite unity universal universe university unjust unkind unknown
unless unlike unlikely unload unlock unmarried unnatural unnecessary unpack unpleasant unpredictable unqualified unreal
unreasonable unrest unsafe unsatisfactory unseen unskilled unstable unsuitable untie until untidy unlikely unusual
unwilling unworthy up uphold upon upper upright upset upside upstairs upward urge urgent
us usage use useful useless user usual utility vacant vacation vacuum vague vain
valiant valid valley valuable value valve vanilla vanish vanity vapor variable variation varied
variety various varnish vary vase vast vat vault veal vegetable vehicle veil vein
velocity velvet vendor venerable vengeance venom venomous ventilator venture venue verb verbal verdict
verge verify verse version versus vertical very vessel veteran veto vex via viaduct
vibrate vibration vice vicinity victim victor victory video view viewer vigor vigorous village
villain vine vineyard violate violence violent violet violin viper virgin virtue virtual
virtue virus visa visible vision visit visitor visor visual vital vitamin vivid vocabulary
vocation voice void volatile volcano volley volt volume voluntary volunteer vomit vote voter
vow vowel voyage vulgar vulnerable vulture wade wage wagon waist wait waiter waitress
wake walk wall walnut wander want war ward warden wardrobe warehouse warfare warm
warmth warn warning warrant warrior warship wash washer waste watch watchful water waterfall
waterproof wave waver wax way we weak weaken weakness wealth wealthy weapon wear
weary weather weave weaver web wedding wedge Wednesday weed week weekday weekend weekly
weep weigh weight weird welcome weld welfare well west western wet whale wharf
what wheat wheel when whenever where whereabouts whereas whereby wherever whether which while
whip whirl whisper whistle white whoever whole wholesale wholesome wholly whom whose why
wicked wide widespread widow width wield wife wild wilderness willful will willing willow
win wind window windmill windowpane wine wing wink winner winter wipe wire wisdom
wise wish wit witch with withdraw wither withhold within without withstand witness wizard
woe wolf woman wonder wonderful wood woodpecker wool word work worker workshop world
worm worry worse worship worst worth worthy wound wrap wrath wreath wreck wreckage
wren wrench wrestle wretch wright wrist write writer writing wrong yard yarn yawn
year yearn yeast yell yellow yelp yes yesterday yet yield yoke yolk yonder
you young youngster your youth zeal zealous zebra zenith zero zest zigzag zinc zone
zoo zoology cryptography computer security monarchy privacy password ciphertext plaintext
decryption encryption zebra matrix columnar railfence vigenere substitution playfair route
""".split()

words = set(w.lower() for w in base_text.split() if w.isalpha() and len(w) >= 2)
expanded = set(words)
for w in list(words):
    if len(w) >= 3:
        expanded.add(w + 's')
        if w.endswith('e'):
            expanded.add(w + 'd')
            expanded.add(w + 'r')
        elif not w.endswith(('y', 's', 'x', 'z', 'ch', 'sh')):
            expanded.add(w + 'ed')
            expanded.add(w + 'ing')
        elif w.endswith('y') and len(w) > 3 and w[-2] not in 'aeiou':
            expanded.add(w[:-1] + 'ies')
            expanded.add(w[:-1] + 'ied')

final_words = sorted(list(set(w for w in expanded if w.isalpha() and len(w) >= 2)))

print(f"Generated {len(final_words)} unique English words.")
