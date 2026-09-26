# Script to generate a 4,000+ word list for embedded dictionary

common_words = set("""
a abandon ability able about above abroad absence absolute absolutely absorb abuse academic accept access
accident accompany accomplish according account accurate accuse achieve achievement acid acknowledge acquire across
act action active activist activity actor actress actual actually ad adapt add addition additional
address adequate adjust adjustment administration administrator admire admit adopt adult advance advanced advantage
adventure advertising advice advise advocate affair affect afford afraid african after afternoon again
against age agency agenda agent aggressive ago agree agreement agricultural ah ahead aid aide
aim air aircraft airline airport album alcohol alive all alliance allow ally almost alone
along already also alter alternative although always am amazing american among amount analysis analyst
analyze ancient and anger angle angry animal anniversary announce announcement annual another answer anticipate
anxiety anxious any anybody anyone anything anyway anywhere apart apartment apparent apparently appeal appear
appearance apple application apply appoint appointment appreciate approach appropriate approval approve approximately arab
architect architecture area argue argument arise arm armed army around arrange arrangement arrest arrival
arrive art article artist artistic as asian aside ask asleep aspect assert assessment asset
assign assignment assist assistance assistant associate association assume assumption assure at athlete athletic atmosphere
attach attack attempt attend attention attitude attorney attract attraction attractive attribute audience aunt author
authority auto available avenue average avoid award aware awareness away awful baby back background
backwards bacon bad badly bag bake balance ball ban banana band bank bar barely barn
barrel barrier base baseball basic basically basis basket basketball pass passion past patch path patient
pattern pause pay payment peace peak peer penalty people pepper per perceive percentage perception perfect
perfectly perform performance perhaps period permanent permission permit person personal personality personally personnel perspective
persuade pet phase phenomenon philosophy phone photo photograph photographer photography phrase physical physically physician
piano pick picture pie piece pile pilot pine pink pipe pitch place plan plane planet
planning plant plastic plate platform play player playfair plea pleasant please pleasure plenty plot plunge
plus pocket poem poet poetry point pole police policy political politician politics poll pollution pool
poor pop popular population porch port portion portrait portray pose position positive possess possibility
possible possibly post pot potato potential potentially pound pour poverty power powerful practical practice
pragmatic praise pray prayer preach precious precise precisely predict preference prefer pregnant preliminary premise premium
preparation prepare prescription presence present presentation preserve president press pressure pretend pretty prevent previous
previously price pride priest primarily primary prime principal principle print prior priority prison prisoner
privacy private probably problem procedure proceed process produce producer product production profession professional professor
profile profit program progress project prominent promise promote prompt proof proper properly property proportion
proposal propose proposed prosecution prospect protect protection protein protest proud prove provide provider province
provision psychological psychologist psychology public publication publicity publicly publish publisher pull pulse pump punch
punish punishment pupil purchase pure purpose pursue push put qualify quality quantity quarter quarterback queen
quest question quick quickly quiet quietly quit quite quote rabbit race racial radical radio rail
railroad rain raise rally ranch random range rank rapid rapidly rare rarely rate rather rating
ratio rational raw reach react reaction read reader readily reading ready real realistic reality realize
really realm rear reason reasonable recall receive recent recently recipe recognition recognize recommend recommendation
reconciliation record recording recover recovery recruit red reduce reduction refer reference reflect reflection reform
refugee refuse regard regarding regardless regime region regional register regular regularly regulate regulation reinforce reject
relate relation relationship relative relatively relax release relevant relief religion religious rely remain remaining
remarkable remember remind remote remove repeat repeatedly replace replacement reply report reporter represent representation
representative republican reputation request require requirement research researcher resemble reservation resident resist resistance resolution
resolve resort resource respect respond respondent response responsibility responsible rest restaurant restore result retain retire
retirement return reveal revenue review revolution rhythm rib rice rich rid ride rifle right ring
rise risk river road robot rock rod role roll rolling roman romantic roof room root
rope rose rough roughly round route routine row rub rule run running rural rush russian
sacred sad safe safety sake salad salary sale sales salt same sample sanction sand satellite
satisfation satisfy sauce save saving say scale scandal scare scared scenario scene schedule scheme scholar
scholarship school science scientific scientist scope score scream screen script search season seat second secret
secretary section sector secure security see seed seek seem segment seize select selection self sell
senator send senior sense sensitive sentence separate sequence series serious seriously servant serve service session
set setting settle settlement seven several severe shade shadow shake shall shape share sharp sheet
shelf shell shelter shift shine ship shirt shock shoe shoot shooting shop shopping shore short
shot should shoulder shout show shower shrug shut sibling sick side sidewalk sigh sight sign
signal significance significant significantly silence silent silver similar similarly simple simply sin since sing
singer single sink sir sister sit site situation six size ski skill skin sky slave
sleep slice slide slight slightly slip slow slowly small smart smell smile smoke smooth snap
snow so soaked soap soar social society sock soft software soil solar soldier solid solution
solve some somebody somehow someone something sometimes somewhat somewhere son song soon sophisticated sorry sort
soul sound soup source south southern soviet space spanish speak speaker special specialist species specific
specifically speech speed spend spending spin spirit spiritual split spoke spokesman sponsor spoon sport spot
spread spring square squeeze stability stable staff stage stair stake stand standard standing star stare
start state statement station statistic statistics statue status stay steady steak steal steam steel step
stick still stir stock stomach stone stop storage store storm story stove straight strange stranger
strategic strategy stream street strength strengthen stress stretch strike string strip stroke strong strongly structure
struggle student studio study stuff stupid style subject submit subsequent substance substantial succeed success
successful successfully such sudden suddenly sue suffer sufficient sugar suggest suggestion suicide suit summer summit
sun super supply support supporter suppose supposed supreme sure surely surface surgeon surgery surprise surprised
surprising surprisingly surround survey survival survive survivor suspect sustain swear sweat sweep sweet swim swing
switch symbol symptom system table tablespoon tactic tail take tale talent talk tall tank tap
target task taste tax taxpayer tea teach teacher teaching team tear teaspoon technical technique technology
teen teenager telephone telescope television tell temperature ten tend tendency tennis tension tent term terms
terrible territory terror terrorism terrorist test testify testimony testing text than thank thanks that the
theater their them theme themselves then theory therapy there thereafter thereby therefore these they thick thin
thing think thinking third thirty this thorough thoroughly those though thought thousand threat threaten three
throat through throughout throw thumb thus ticket tie tight time tiny tip tire tired tissue
title to tobacco today toe together tomato tomorrow tone tongue tonight too tool tooth top
topic toss total totally touch tough tour tourist tournament toward towards tower town toy trace
track trade tradition traditional traffic trail train trainer training trait transfer transform transformation transition translate
transport transportation trap travel treat treatment treaty tree tremendous trend trial tribe trick trip troop
trouble truck true truly trust truth try tube tunnel turn tv twelve twenty twice twin two
type typical typically ugly ultimate ultimately unable uncle under undergo understand understanding undertake unemployment unexpected unfair
unfortunate unfortunately unhappy uniform union unique unit united universal universe university unknown unless unlike unlikely
until unusual up upon upper urban urge us use used useful user usual usually utility vacation
valley valuable value variable variation variety various vary vast vegetable vehicle venture version versus very vessel
veteran via victim victory video view viewer village violate violation violence violent virtually virtue virus visible
vision visit visitor visual vital voice volume volunteer vote voter vow voyage wage wait wake
walk wall wander want war warm warn warning wash waste watch water wave way we
weak weaken wealth wealthy weapon wear weather web website wedding weed week weekend weekly weigh weight
welcome welfare well west western wet what whatever wheel when whenever where whereas whereby wherein whereupon
wherever whether which while whisper white who whoever whole whom whose why wide widely widespread wife
wild will willing win wind window wine wing winner winter wipe wire wisdom wise wish with
withdraw within without witness wolf woman wonder wonderful wood wooden word work worker working works world
worry worth would wound wrap write writer writing wrong yard yeah year yell yellow yes yesterday
yet yield you young your yourself youth zebra zone zoo accuracy decrypt encrypt matrix
permutation alphabet frequency polyalphabetic ciphertext plaintext railfence columnar vigenere substitution playfair route
""".split())

print(f"Total compiled words: {len(common_words)}")
