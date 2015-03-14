"""
featureDetectionTests.py
~~~~~~~~~~~~~~~

Test functions for featureDetection

"""


import featureDetection


vectorizedLine = [(0.20967577397823334, 0.1902720332145691),
(0.05081852153867609, 0.8577813371035022), (0.011105588342113507,
0.8821657880694562), (0.02297810045194936, 0.8922985787352331),
(0.020698199507621994, 0.892361936673728), (0.030200788143485396,
0.8539393566240734), (0.0261243924624738, 0.8266816883351211),
(0.029497509491946586, 0.828271116047942), (0.031655814683353774,
0.816222508669854), (0.03328579872004682, 0.8031342793236256),
(0.034883411099996764, 0.8106357334610511), (0.03652117768032658,
0.8222913365779304), (0.03676393543249999, 0.8093623192072024),
(0.03740214720355422, 0.8029397095292662), (0.03790012288508744,
0.8118374628273521), (0.03719518974132318, 0.7859601940822587),
(0.03617659049944581, 0.7737452598598185), (0.03561812955047603,
0.7658831634322166), (0.034257610593265465, 0.7503042759034653),
(0.03208762588018608, 0.719306352906953), (0.01930155937407832,
0.6692844428700935), (0.02801636342792103, 0.6857269661770568),
(0.01531872369196515, 0.6414583498207019), (0.012785298764572978,
0.6023812266159518)]

def testMagnitude():
    print "Testing magnitude()... ",
    (a, b) = (0,0), (3,4)
    assert(featureDetection.magnitude(a,b) == 5.0)
    print "Passed!"

def testSplitToStrokes():
    print "Testing splitToStrokes()... ",
    a1 =[
(0.1416589915752411, 0.3047013580799103, 4502.191), (0.14114759862422943,
0.30588409304618835, 4502.199), (0.1409430354833603, 0.30632761120796204,
4502.207), (0.140533909201622, 0.30706682801246643, 4502.215),
(0.14032934606075287, 0.30736249685287476, 4502.223), (0.1399202197790146,
0.30765819549560547, 4502.231), (0.13971565663814545, 0.3079538643360138,
4502.239), (0.13930653035640717, 0.30839741230010986, 4502.247),
(0.13910196721553802, 0.30884093046188354, 4502.255), (0.13889741897583008,
0.3097279667854309, 4502.263), (0.13899970054626465, 0.3112064003944397,
4502.271), (0.13961337506771088, 0.31357184052467346, 4502.279),
(0.14114759862422943, 0.3178592622280121, 4502.287), (0.1437046080827713,
0.3240686058998108, 4502.295), (0.14881865680217743, 0.3347131907939911,
4502.303), (0.15669427812099457, 0.34994086623191833, 4502.311),
(0.16508130729198456, 0.36487284302711487, 4502.319), (0.17162728309631348,
0.3761088252067566, 4502.327), (0.18103712797164917, 0.39237138628959656,
4502.335), (0.190651535987854, 0.4090774655342102, 4502.343),
(0.20026592910289764, 0.4256357252597809, 4502.351), (0.20589137077331543,
0.4358367919921875, 4502.359), (0.2142784148454666, 0.450177401304245,
4502.367), (0.22205175459384918, 0.4628917872905731, 4502.375),
(0.22941598296165466, 0.4739798903465271, 4502.383), (0.23667791485786438,
0.48329392075538635, 4502.391), (0.24414442479610443, 0.4911295175552368,
4502.399), (0.25242915749549866, 0.4974866807460785, 4502.407),
(0.2617367208003998, 0.5028089880943298, 4502.415), (0.27196481823921204,
0.5070964097976685, 4502.423), (0.2833179831504822, 0.510348916053772,
4502.431), (0.2954894006252289, 0.5131579041481018, 4502.439),
(0.3081722557544708, 0.5152276754379272, 4502.447), (0.32065051794052124,
0.517001748085022, 4502.455), (0.3329242169857025, 0.5181844830513, 4502.463),
(0.3447887897491455, 0.5193672180175781, 4502.471), (0.3560396730899811,
0.5202543139457703, 4502.479), (0.36268794536590576, 0.520697832107544,
4502.487), (0.3727114796638489, 0.5209934711456299, 4502.495),
(0.3855988681316376, 0.5211413502693176, 4502.503), (0.39480412006378174,
0.5204021334648132, 4502.511), (0.4039071202278137, 0.5187758803367615,
4502.519), (0.4130101203918457, 0.5161147117614746, 4502.527),
(0.4221131205558777, 0.5125665068626404, 4502.535), (0.43131840229034424,
0.5079834461212158, 4502.543), (0.44062596559524536, 0.5025132894515991,
4502.551), (0.44972896575927734, 0.4963039755821228, 4502.559),
(0.45842283964157104, 0.4893554151058197, 4502.567), (0.4662984609603882,
0.4821111857891083, 4502.575), (0.4703896939754486, 0.47708457708358765,
4502.583), (0.4760151505470276, 0.4699881672859192, 4502.591),
(0.4805155098438263, 0.46274393796920776, 4502.599), (0.48378849029541016,
0.45579537749290466, 4502.607), (0.4858340919017792, 0.4486989974975586,
4502.615), (0.4867546260356903, 0.44145476818084717, 4502.623),
(0.48655006289482117, 0.43421053886413574, 4502.631), (0.48593637347221375,
0.42652276158332825, 4502.639), (0.484299898147583, 0.4160260260105133,
4502.647), (0.4832770824432373, 0.40966883301734924, 4502.655),
(0.48133373260498047, 0.39680662751197815, 4502.663), (0.480106383562088,
0.3855706751346588, 4502.671), (0.47898128628730774, 0.3734476566314697,
4502.679), (0.47857216000556946, 0.36487284302711487, 4502.687),
(0.4777539074420929, 0.35274985432624817, 4502.695), (0.4770379364490509,
0.3409225344657898, 4502.703), (0.47652652859687805, 0.3292430639266968,
4502.711), (0.4760151505470276, 0.3181549310684204, 4502.719),
(0.4757083058357239, 0.3075103461742401, 4502.727), (0.47550374269485474,
0.29745712876319885, 4502.735), (0.4757083058357239, 0.2876995801925659,
4502.743), (0.4764242470264435, 0.27838557958602905, 4502.751),
(0.4781630337238312, 0.2658190429210663, 4502.759), (0.4809246063232422,
0.25650501251220703, 4502.767), (0.48491358757019043, 0.24689532816410065,
4502.775), (0.4916641116142273, 0.2338852733373642, 4502.783),
(0.4992328882217407, 0.22383205592632294, 4502.791), (0.5081313252449036,
0.21407450735569, 4502.799), (0.5181548595428467, 0.2049083411693573, 4502.807),
(0.5253145098686218, 0.19988173246383667, 4502.815), (0.5356448888778687,
0.1927853375673294, 4502.823), (0.5461798310279846, 0.18687167763710022,
4502.831), (0.5565101504325867, 0.1825842708349228, 4502.839),
(0.5631584525108337, 0.1811058521270752, 4502.847), (0.5763526558876038,
0.17770549654960632, 4502.855), (0.5855579376220703, 0.1774098128080368,
4502.863), (0.5945586562156677, 0.17874039709568024, 4502.871),
(0.6068323850631714, 0.18199290335178375, 4502.879), (0.6163445115089417,
0.18701951205730438, 4502.887), (0.6262657046318054, 0.19367238879203796,
4502.895), (0.6365960836410522, 0.20209935307502747, 4502.903),
(0.6513245105743408, 0.2155529260635376, 4502.911), (0.6632913947105408,
0.22856298089027405, 4502.919), (0.6753605604171753, 0.24364282190799713,
4502.927), (0.6870205402374268, 0.260940283536911, 4502.935),
(0.6939756274223328, 0.27395033836364746, 4502.943), (0.7041014432907104,
0.2936132550239563, 4502.951), (0.7127953171730042, 0.31475457549095154,
4502.959), (0.7196481823921204, 0.3375221788883209, 4502.967),
(0.7244553565979004, 0.36117681860923767, 4502.975), (0.7274215221405029,
0.38586634397506714, 4502.983), (0.7284443378448486, 0.4115907847881317,
4502.991), (0.7280352115631104, 0.4376108944416046, 4502.999),
(0.7263987064361572, 0.4640745222568512, 4503.007), (0.7239439487457275,
0.49098166823387146, 4503.015), (0.7213869094848633, 0.5174453258514404,
4503.023), (0.7186253666877747, 0.5433175563812256, 4503.031),
(0.7160683274269104, 0.5677114129066467, 4503.039), (0.7148409485816956,
0.5816085338592529, 4503.047), (0.7136135697364807, 0.5934358239173889,
4503.055), (0.7116702198982239, 0.610141932964325, 4503.063),
(0.7094200849533081, 0.6237433552742004, 4503.071), (0.7068630456924438,
0.6340922713279724, 4503.079), (0.7035900354385376, 0.6411886215209961,
4503.087), (0.6984760165214539, 0.6472501754760742, 4503.095),
(0.6929528713226318, 0.6469544768333435, 4503.103), (0.6864068508148193,
0.6445890069007874, 4503.111), (0.6789403557777405, 0.6407451033592224,
4503.119), (0.6676895022392273, 0.6339443922042847, 4503.127),
(0.6676895022392273, 0.6339443922042847, 4503.135)
    ]
    a2 = [
(0.17582079768180847, 0.4846244752407074, 4696.696), (0.17704817652702332,
0.47930219769477844, 4696.704), (0.1774573028087616, 0.4801892340183258,
4696.712), (0.1767413318157196, 0.4816676378250122, 4696.72),
(0.17551396787166595, 0.4828503727912903, 4696.728), (0.17490027844905853,
0.4853636920452118, 4696.736), (0.17490027844905853, 0.4893554151058197,
4696.744), (0.17561624944210052, 0.494825541973114, 4696.752),
(0.17694589495658875, 0.5020697712898254, 4696.76), (0.1788892298936844,
0.5112359523773193, 4696.768), (0.1812416911125183, 0.521880567073822,
4696.776), (0.1851283609867096, 0.537551760673523, 4696.784),
(0.19024240970611572, 0.5549970269203186, 4696.792), (0.19873172044754028,
0.5801301002502441, 4696.8), (0.20722103118896484, 0.600975751876831, 4696.808),
(0.21693770587444305, 0.6210821866989136, 4696.816), (0.2278817594051361,
0.6401537656784058, 4696.824), (0.24015547335147858, 0.6575990319252014,
4696.832), (0.24925845861434937, 0.6673566102981567, 4696.84),
(0.26255497336387634, 0.6815493702888489, 4696.848), (0.27124884724617004,
0.6884979009628296, 4696.856), (0.2839316725730896, 0.6985511779785156,
4696.864), (0.2961030900478363, 0.7063867449760437, 4696.872),
(0.3030582070350647, 0.7093436121940613, 4696.88), (0.31328627467155457,
0.7142223715782166, 4696.888), (0.31778663396835327, 0.716439962387085,
4696.896), (0.31778663396835327, 0.716439962387085, 4696.904),
(0.3674951493740082, 0.23654642701148987, 4697.496), (0.3684156835079193,
0.236102893948555, 4697.504), (0.3694384694099426, 0.23432880640029907,
4697.512), (0.36974531412124634, 0.23373743891716003, 4697.52),
(0.3699498772621155, 0.23285038769245148, 4697.528), (0.37179094552993774,
0.23151980340480804, 4697.536), (0.3746547996997833, 0.22974571585655212,
4697.544), (0.3785414695739746, 0.2272324115037918, 4697.552),
(0.38324639201164246, 0.22427557408809662, 4697.56), (0.38917869329452515,
0.2210230678319931, 4697.568), (0.39644062519073486, 0.21791839599609375,
4697.576), (0.40769150853157043, 0.21348313987255096, 4697.584),
(0.42088574171066284, 0.20919574797153473, 4697.592), (0.4363301694393158,
0.20594322681427002, 4697.6), (0.4534110724925995, 0.20372560620307922,
4697.608), (0.47202616930007935, 0.20254287123680115, 4697.616),
(0.49810779094696045, 0.20283855497837067, 4697.624), (0.5183594226837158,
0.20549970865249634, 4697.632), (0.5390201210975647, 0.2103784680366516,
4697.64), (0.5593740344047546, 0.21762271225452423, 4697.648),
(0.5792165398597717, 0.22782377898693085, 4697.656), (0.6051958799362183,
0.24586044251918793, 4697.664), (0.6232995986938477, 0.2658190429210663,
4697.672), (0.6405850648880005, 0.29169130325317383, 4697.68),
(0.6569499969482422, 0.32199880480766296, 4697.688), (0.6718829870223999,
0.3560023605823517, 4697.696), (0.6795540452003479, 0.3801005184650421,
4697.704), (0.6903958320617676, 0.41410407423973083, 4697.712),
(0.695100724697113, 0.4346540570259094, 4697.72), (0.6992942690849304,
0.45136013627052307, 4697.728), (0.7026695013046265, 0.4636309742927551,
4697.736), (0.7080904245376587, 0.4804849326610565, 4697.744),
(0.711874783039093, 0.4908338189125061, 4697.752), (0.711874783039093,
0.4908338189125061, 4697.76)     
    ]
    a3 = [(0.14390917122364044,
0.5909225344657898, 4754.706), (0.1437046080827713, 0.5966883301734924,
4754.716), (0.14482970535755157, 0.6040804386138916, 4754.724),
(0.14738672971725464, 0.6145771741867065, 4754.732), (0.15076199173927307,
0.6222649216651917, 4754.74), (0.1551600694656372, 0.6311354041099548,
4754.748), (0.16139920055866241, 0.6411886215209961, 4754.756),
(0.16937710344791412, 0.6516854166984558, 4754.764), (0.17899151146411896,
0.6632170081138611, 4754.772), (0.19423136115074158, 0.6811058521270752,
4754.78), (0.21182367205619812, 0.700768768787384, 4754.788),
(0.2251201868057251, 0.7137788534164429, 4754.796), (0.24445126950740814,
0.7315198183059692, 4754.804), (0.26357778906822205, 0.7474867105484009,
4754.812), (0.2752377986907959, 0.755322277545929, 4754.82),
(0.28587502241134644, 0.7613837718963623, 4754.828), (0.301319420337677,
0.7704021334648132, 4754.836), (0.31502506136894226, 0.7763158082962036,
4754.844), (0.3269919157028198, 0.7792726159095764, 4754.852),
(0.3375268578529358, 0.7811945676803589, 4754.86), (0.3375268578529358,
0.7811945676803589, 4754.868), (0.8307251930236816, 0.8545239567756653,
4755.184), (0.8326684832572937, 0.8440272212028503, 4755.192),
(0.8255088329315186, 0.839296281337738, 4755.2), (0.8216221928596497,
0.8370786309242249, 4755.208), (0.8167126774787903, 0.8324955701828003,
4755.216), (0.81078040599823, 0.8261383771896362, 4755.224),
(0.8048481345176697, 0.8180071115493774, 4755.232), (0.7985066771507263,
0.8083974123001099, 4755.24), (0.7915515899658203, 0.7977527976036072,
4755.248), (0.7838805317878723, 0.7863690257072449, 4755.256),
(0.7722204923629761, 0.7687758803367615, 4755.264), (0.7549350261688232,
0.7415730357170105, 4755.272), (0.7396951913833618, 0.7179183959960938,
4755.28), (0.7229211330413818, 0.6927853226661682, 4755.288),
(0.7038968801498413, 0.6654346585273743, 4755.296), (0.6834407448768616,
0.6366055607795715, 4755.304), (0.6528587341308594, 0.5975754261016846,
4755.312), (0.627083957195282, 0.567267894744873, 4755.32), (0.5991612672805786,
0.5372560620307922, 4755.328), (0.569090723991394, 0.5076877474784851,
4755.336), (0.5374859571456909, 0.47738024592399597, 4755.344),
(0.5046537518501282, 0.44736841320991516, 4755.352), (0.4714125096797943,
0.41735658049583435, 4755.36), (0.4391940236091614, 0.3863098621368408,
4755.368), (0.4088166058063507, 0.3560023605823517, 4755.376),
(0.39132657647132874, 0.3364872932434082, 4755.384), (0.3761890232563019,
0.3185984492301941, 4755.392), (0.3546077609062195, 0.2933175563812256, 4755.4),
(0.34397053718566895, 0.27912476658821106, 4755.408), (0.33558350801467896,
0.2680366635322571, 4755.416), (0.33558350801467896, 0.2680366635322571,
4755.424), (0.5244962573051453, 0.18894144892692566, 4755.784),
(0.5250076651573181, 0.17800118029117584, 4755.792), (0.5250076651573181,
0.17386162281036377, 4755.8), (0.5252122282981873, 0.1748965084552765,
4755.808), (0.5264396071434021, 0.1741573065519333, 4755.816),
(0.5294057726860046, 0.1729745715856552, 4755.824), (0.5342129468917847,
0.1719396859407425, 4755.832), (0.5396338105201721, 0.17105263471603394,
4755.84), (0.5461798310279846, 0.1697220653295517, 4755.848),
(0.5536463260650635, 0.16868716478347778, 4755.856), (0.5619310736656189,
0.16735659539699554, 4755.864), (0.5744093060493469, 0.16543465852737427,
4755.872), (0.5886263847351074, 0.16380839049816132, 4755.88),
(0.6044799089431763, 0.16218213737010956, 4755.888), (0.6214585304260254,
0.16144293546676636, 4755.896), (0.6458013653755188, 0.161295086145401,
4755.904), (0.6657461524009705, 0.16336487233638763, 4755.912),
(0.6862022876739502, 0.16780011355876923, 4755.92), (0.7073744535446167,
0.17504435777664185, 4755.928), (0.7280352115631104, 0.1858367770910263,
4755.936), (0.755241870880127, 0.20579539239406586, 4755.944),
(0.7740615606307983, 0.22752809524536133, 4755.952), (0.7843919396400452,
0.244825541973114, 4755.96), (0.7981998324394226, 0.2717326879501343, 4755.968),
(0.8088370561599731, 0.30011826753616333, 4755.976), (0.8126214742660522,
0.31800708174705505, 4755.984), (0.8126214742660522, 0.31800708174705505,
4755.992)
    ]
    assert(len(featureDetection.splitToStrokes(a1)) == 1) 
    assert(len(featureDetection.splitToStrokes(a2)) == 2) 
    assert(len(featureDetection.splitToStrokes(a3)) == 3) 
    print "Passed!"

