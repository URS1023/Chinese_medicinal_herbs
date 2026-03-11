// pages/list1/list1.js
Page({
  data: {
    filter: 'all',       // 当前过滤条件
    currentPage: 1,      // 当前页码
    totalPages: 3,       // 总页数（需根据实际数据调整）
    pageList: [1, 2, 3], // 页码列表
    showModal: false,    // 模态框显示状态
    currentHerb: {},     // 当前查看的药材信息
    // 模拟药材数据（需替换为实际接口数据）
    herbs: [
      {
        "id": 1,
        "name": "白参",
        "english_name": "White Ginseng",
        "image_path": "/images/picture/白参.jpg",
        "properties": "味甘，微苦，性微寒。 \n归肺，脾经。",
        "effects": "大补元气 ,补脾益肺,生津止渴,安神益智\n",
        "description": "白参饮片呈长圆形或不规则的薄片，色泽为微白的黄色。\n质地：质脆体实。\n断面：断面白色，有放射状花纹。\n气味：气香，味甘而微苦。",
        "season": "秋季",
        "similar_herbs": [
            "沙参",
            "沙参"
        ]
    },
    {
        "id": 2,
        "name": "北沙参",
        "english_name": "radix glehniae",
        "image_path": "/images/picture/北沙参.jpg",
        "properties": "甘、微苦，微寒。归肺、胃经",
        "effects": "养阴清肺，益胃生津。用于肺热燥咳，劳嗽痰血，胃阴不足，热病津伤，咽干口渴。",
        "description": "本品呈细长圆柱形，偶有分枝，长15～45cm，直径0.4～1.2cm。表面淡黄白色，略粗糙，偶有残存外皮，不去外皮的表面黄棕色。全体有细纵皱纹和纵沟，并有棕黄色点状细根痕；顶端常留有黄棕色根茎残基；上端稍细，中部略粗，下部渐细。质脆，易折断，断面皮部浅黄白色，木部黄色。气特异，味微甘。\n",
        "season": "冬季",
        "similar_herbs": [
            "黄芪",
            "明党参"
        ]
    },
    {
        "id": 3,
        "name": "丹参",
        "english_name": "Salvia miltiorrhiza",
        "image_path": "/images/picture/丹参.jpg",
        "properties": "苦，微寒。归心、肝经。",
        "effects": "活血祛瘀，通经止痛，清心除烦，凉血消痈。用于胸痹心痛，脘腹胁痛，癥瘕积聚，热痹疼痛，心烦不眠，月经不调，痛经经闭，疮疡肿痛。",
        "description": "本品呈类圆形或椭圆形的厚片。外表皮棕红色或暗棕红色，粗糙，具纵皱纹。切面有裂隙或略平整而致密，有的呈角质样，皮部棕红色，木部灰黄色或紫褐色，有黄白色放射状纹理。气微，味微苦涩。",
        "season": "夏季",
        "similar_herbs": [
            "莪术",
            "山豆根"
        ]
    },
    {
        "id": 4,
        "name": "党参",
        "english_name": "Codonopsis pilosula",
        "image_path": "/images/picture/党参.jpg",
        "properties": "甘，平。归脾、肺经。",
        "effects": "健脾益肺，养血生津。用于脾肺气虚，食",
        "description": "本品呈类圆形的厚片。外表皮灰黄色、黄棕色至灰棕色，有时可见根头部有多数疣状突起的茎痕和芽。切面皮部淡棕黄色至黄棕色，木部淡黄色至黄色，有裂隙或放射状纹理。有特殊香气，味微甜。",
        "season": "春季",
        "similar_herbs": [
            "西洋参"
        ]
    },
    {
        "id": 5,
        "name": "苦参",
        "english_name": "Sophora flavescens",
        "image_path": "/images/picture/苦参.jpg",
        "properties": "苦，寒。归心、肝、胃、大肠、膀胱经。",
        "effects": "清热燥湿，杀虫，利尿。用于热痢，便血，黄疸尿闭，赤白带下，阴肿阴痒，湿疹，湿疮，皮肤瘙痒，疥癣麻风；外治滴虫性阴道炎。",
        "description": "本品呈类圆形或不规则形的厚片。外表皮灰棕色或棕黄色，有时可见横长皮孔样突起，外皮薄，常破裂反卷或脱落，脱落处显黄色或棕黄色，光滑。切面黄白色，纤维性，具放射状纹理和裂隙，有的可见同心性环纹。气微，味极苦。",
        "season": "夏季",
        "similar_herbs": [
            "西洋参",
            "北豆根",
            "山豆根"
        ]
    },
    {
        "id": 6,
        "name": "明党参",
        "english_name": "Changium smyrnioides",
        "image_path": "/images/picture/明党参.jpg",
        "properties": "甘、微苦，微寒。归肺、脾、肝经。",
        "effects": "润肺化痰，养阴和胃，平肝，解毒。用于肺热咳嗽，呕吐反胃，食少口干，目赤眩晕，疔毒疮疡。",
        "description": "本品呈圆形或类圆形厚片。外表皮黄白色，光滑或有纵沟纹。切面黄白色或淡棕色，半透明，角质样，木部类白色，有的与皮部分离。气微，味淡",
        "season": "夏季",
        "similar_herbs": [
            "南沙参",
            "莪术",
            "人参"
        ]
    },
    {
        "id": 7,
        "name": "南沙参",
        "english_name": "Nansha ginseng",
        "image_path": "/images/picture/南沙参.jpg",
        "properties": "甘，微寒。归肺、胃经。",
        "effects": "养阴清肺，益胃生津，化痰，益气。用于肺热燥咳，阴虚劳嗽，干咳痰黏，胃阴不足，食少呕吐，气阴不足，烦热口干。",
        "description": "本品呈圆形、类圆形或不规则形厚片。外表皮黄白色或淡棕黄色，切面黄白色，有不规则裂隙。气微，味微甘。鉴别，检查，浸出物，同药材。",
        "season": "春季",
        "similar_herbs": [
            "太子参",
            "白参"
        ]
    },
    {
        "id": 8,
        "name": "人参",
        "english_name": "ginseng",
        "image_path": "/images/picture/人参.jpg",
        "properties": "甘、微苦，微温。归脾、肺、心、肾经。",
        "effects": "大补元气，复脉固脱，补脾益肺，生津养血，安神益智。用于体虚欲脱，肢冷脉微，脾虚食少，肺虚喘咳，津伤口渴，内热消渴，气血亏虚，久病虚羸，惊悸失眠，阳痿宫冷。",
        "description": "本品呈圆形或类圆形薄片。外表皮灰黄色。切面淡黄白色或类白色，显粉性，形成层环纹棕黄色，皮部有黄棕色的点状树脂道及放射性裂隙。体轻，质脆。香气特异，味微苦、甘。",
        "season": "冬季",
        "similar_herbs": [
            "北豆根"
        ]
    },
    {
        "id": 9,
        "name": "三七",
        "english_name": "Panax notoginseng",
        "image_path": "/images/picture/三七.jpg",
        "properties": "甘、微苦，温。归肝、胃经。",
        "effects": "散瘀止血，消肿定痛。用于咯血，吐血，衄血，便血，崩漏，外伤出血，胸腹刺痛，跌扑肿痛。",
        "description": "表面灰褐色或灰黄色，有断续的纵皱纹和支根痕。顶端有茎痕，周围有瘤状突起。体重，质坚实，断面灰绿色、黄绿色或灰白色，木部微呈放射状排列。气微，味苦回甜。",
        "season": "冬季",
        "similar_herbs": [
            "南沙参",
            "三七",
            "苦参"
        ]
    },
    {
        "id": 10,
        "name": "沙参",
        "english_name": "Adenophora Root",
        "image_path": "/images/picture/沙参.jpg",
        "properties": "味甘、微苦，性微寒。归肺、胃经。\n",
        "effects": " 养阴清热，润肺化痰，益胃生津。用于阴虚久咳，痨嗽痰血，燥咳痰少，虚热喉痹，津伤口渴。",
        "description": "沙参为圆形或类圆形厚片,，表面黄白色或类白色,，有多数不规则裂隙,，呈花纹状。周边淡棕黄色,，皱缩。质轻。无臭,，味微甘。蜜沙参形如南沙参片,，表面橙黄色或焦黄色,，偶见焦斑,，味甜。",
        "season": "秋季",
        "similar_herbs": [
            "桔梗"
        ]
    },
    {
        "id": 11,
        "name": "太子参",
        "english_name": "radix pseudostellariae",
        "image_path": "/images/picture/太子参.jpg",
        "properties": "甘、微苦，平。归脾、肺经。",
        "effects": "益气健脾，生津润肺。用于脾虚体倦，食欲不振，病后虚弱，气阴不足，自汗口渴，肺燥干咳。",
        "description": "本品呈细长纺锤形或细长条形，稍弯曲，长3～10cm，直径0.2～0.6cm。表面灰黄色至黄棕色，较光滑，微有纵皱纹，凹陷处有须根痕。顶端有茎痕。质硬而脆，断面较平坦，周边淡黄棕色，中心淡黄白色，角质样。气微，味微甘。",
        "season": "冬季",
        "similar_herbs": [
            "玉竹",
            "沙参",
            "党参"
        ]
    },
    {
        "id": 12,
        "name": "西洋参",
        "english_name": "Panax quinquefolius L",
        "image_path": "/images/picture/西洋参.jpg",
        "properties": "甘、微苦，凉。归心、肺、肾经。",
        "effects": "补气养阴，清热生津。用于气虚阴亏，虚热烦倦，咳喘痰血，内热消渴，口燥咽干。",
        "description": "本品呈长圆形或类圆形薄片。外表皮浅黄褐色。切面淡黄白至黄白色，形成层环棕黄色，皮部有黄棕色点状树脂道，近形成层环处较多而明显，木部略呈放射状纹理。气微而特异，味微苦、甘。",
        "season": "冬季",
        "similar_herbs": [
            "板蓝根",
            "人参",
            "当归"
        ]
    },
    {
        "id": 13,
        "name": "玉竹",
        "english_name": "bamboo",
        "image_path": "/images/picture/玉竹.jpg",
        "properties": "甘，微寒。归肺、胃经。",
        "effects": "养阴润燥，生津止渴。用于肺胃阴伤，燥热咳嗽，咽干口渴，内热消渴。",
        "description": "本品呈不规则厚片或段。外表皮黄白色至淡黄棕色，半透明，有时可见环节。切面角质样或显颗粒性。气微，味甘，嚼之发黏。",
        "season": "冬季",
        "similar_herbs": [
            "太子参",
            "明党参"
        ]
    },
    {
        "id": 14,
        "name": "麦冬",
        "english_name": "Ophiopogon japonicus",
        "image_path": "/images/picture/麦冬.jpg",
        "properties": "甘、微苦，微寒。归心、肺、胃经。",
        "effects": "养阴生津，润肺清心。用于肺燥干咳，阴虚痨嗽，喉痹咽痛，津伤口渴，内热消渴，心烦失眠，肠燥便秘。",
        "description": "本品形如麦冬，或为轧扁的纺锤形块片。表面淡黄色或灰黄色，有细纵纹。质柔韧，断面黄白色，半透明，中柱细小。气微香，味甘、微苦。",
        "season": "夏季",
        "similar_herbs": [
            "南沙参"
        ]
    },
    {
        "id": 15,
        "name": "大血藤",
        "english_name": "Sargentgloryvine Stem",
        "image_path": "/images/picture/大血藤.jpg",
        "properties": "苦，平。归大肠、肝经。",
        "effects": "清热解毒，活血，祛风止痛。用于肠痈腹痛，热毒疮疡，经闭，痛经，跌扑肿痛，风湿痹痛。",
        "description": "本品为类椭圆形的厚片。外表皮灰棕色，粗糙。切面皮部红棕色，有数处向内嵌入木部，木部黄白色，有多数导管孔射线呈放射状排列。气微，味微涩",
        "season": "春季",
        "similar_herbs": [
            "黄芩"
        ]
    },
    {
        "id": 16,
        "name": "当归",
        "english_name": "Danggui",
        "image_path": "/images/picture/当归.jpg",
        "properties": "甘、辛，温。归肝、心、脾经。",
        "effects": "补血活血，调经止痛，润肠通便。用于血虚萎黄，眩晕心悸，月经不调，经闭痛经，虚寒腹痛，风湿痹痛，跌扑损伤，痈疽疮疡，肠燥便秘。酒当归活血通经。用于经闭痛经，风湿痹痛，跌扑损伤。",
        "description": "本品呈类圆形、椭圆形或不规则薄片。外表皮浅棕色至棕褐色。切面浅棕黄色或黄白色，平坦，有裂隙，中间有浅棕色的形成层环，并有多数棕色的油点，香气浓郁，味甘、辛、微苦。",
        "season": "冬季",
        "similar_herbs": [
            "麦冬",
            "北沙参"
        ]
    },
    {
        "id": 17,
        "name": "板蓝根",
        "english_name": "Radix isatidis",
        "image_path": "/images/picture/板蓝根.jpg",
        "properties": "苦，寒。归心、胃经。",
        "effects": "清热解毒，凉血利咽。用于温疫时毒，发热咽痛，温毒发斑，痄腮，烂喉丹痧，大头瘟疫，丹毒，痈肿。",
        "description": "本品呈圆形的厚片。外表皮淡灰黄色至淡棕黄色，有纵皱纹。切面皮部黄白色，木部黄色。气微，味微甜后苦涩。",
        "season": "秋季",
        "similar_herbs": []
    },
    {
        "id": 18,
        "name": "北豆根",
        "english_name": "RHIZOMA MENISPERMI",
        "image_path": "/images/picture/北豆根.jpg",
        "properties": "苦，寒；有小毒。归肺、胃、大肠经。",
        "effects": "清热解毒，祛风止痛。用于咽喉肿痛，热毒泻痢，风湿痹痛。",
        "description": "本品为不规则的圆形厚片。表面淡黄色至棕褐色，木部淡黄色，呈放射状排列，纤维性，中心有髓，白色。气微，味苦。",
        "season": "夏季",
        "similar_herbs": []
    },
    {
        "id": 19,
        "name": "知母",
        "english_name": "rhizoma anemarrhenae",
        "image_path": "/images/picture/知母.jpg",
        "properties": "苦、甘，寒。归肺、胃、肾经。",
        "effects": "清热泻火，滋阴润燥。用于外感热病，高热烦渴，肺热燥咳，骨蒸潮热，内热消渴，肠燥便秘。",
        "description": "本品呈不规则类圆形的厚片。外表皮黄棕色或棕色，可见少量残存的黄棕色叶基纤维和凹陷或突起的点状根痕。切面黄白色至黄色。气微，味微甜、略苦，嚼之带黏性。",
        "season": "冬季",
        "similar_herbs": [
            "知母",
            "南沙参",
            "当归"
        ]
    },
    {
        "id": 20,
        "name": "桔梗",
        "english_name": "Platycodon grandiflorum",
        "image_path": "/images/picture/桔梗.jpg",
        "properties": "苦、辛，平。归肺经。",
        "effects": "宣肺，利咽，祛痰，排脓。用于咳嗽痰多，胸闷不畅，咽痛音哑，肺痈吐脓。",
        "description": "本品呈椭圆形或不规则厚片。外皮多已除去或偶有残留。切面皮部黄白色，较窄；形成层环纹明显，棕色；木部宽，有较多裂隙。气微，味微甜后苦。",
        "season": "春季",
        "similar_herbs": [
            "玉竹",
            "山豆根"
        ]
    },
    {
        "id": 21,
        "name": "莪术",
        "english_name": "Zedoary",
        "image_path": "/images/picture/莪术.jpg",
        "properties": "辛、苦，温。归肝、脾经。",
        "effects": "行气破血，消积止痛。用于癥瘕痞块，瘀血经闭，胸痹心痛，食积胀痛。",
        "description": "本品呈类圆形或椭圆形的厚片。外表皮灰黄色或灰棕色，有时可见环节或须根痕。切面黄绿色、黄棕色或棕褐色，内皮层环纹明显，散在“筋脉”小点。气微香，味微苦而辛。",
        "season": "秋季",
        "similar_herbs": [
            "党参"
        ]
    },
    {
        "id": 22,
        "name": "黄芪",
        "english_name": "Astragalus mongholicus",
        "image_path": "/images/picture/黄芪.jpg",
        "properties": "甘，微温。归肺、脾经。",
        "effects": "补气升阳，固表止汗，利水消肿，生津养血，行滞通痹，托毒排脓，敛疮生肌。用于气虚乏力，食少便溏，中气下陷，久泻脱肛，便血崩漏，表虚自汗，气虚水肿，内热消渴，血虚萎黄，半身不遂，痹痛麻木，痈疽难溃，久溃不敛。",
        "description": "本品呈类圆形或椭圆形的厚片，外表皮黄白色至淡棕褐色，可见纵皱纹或纵沟。切面皮部黄白色，木部淡黄色，有放射状纹理及裂隙，有的中心偶有枯朽状，黑褐色或呈空洞。气微，味微甜，嚼之有豆腥味。",
        "season": "秋季",
        "similar_herbs": [
            "桔梗"
        ]
    },
    {
        "id": 23,
        "name": "前胡",
        "english_name": "Saposhnikovia divaricata",
        "image_path": "/images/picture/前胡.jpg",
        "properties": "苦、辛，微寒。归肺经。",
        "effects": "降气化痰，散风清热。用于痰热喘满，咯痰黄稠，风热咳嗽痰多。",
        "description": "本品呈类圆形或不规则形的薄片。外表皮黑褐色或灰黄色，有时可见残留的纤维状叶鞘残基。切面黄白色至淡黄色，皮部散有多数棕黄色油点，可见一棕色环纹及放射状纹理。气芳香，味微苦、辛。",
        "season": "冬季",
        "similar_herbs": [
            "三七",
            "玉竹",
            "人参"
        ]
    },
    {
        "id": 24,
        "name": "黄芩",
        "english_name": "Scutellaria baicalensis",
        "image_path": "/images/picture/黄芩.jpg",
        "properties": "苦，寒。归肺、胆、脾、大肠、小肠经。",
        "effects": "清热燥湿，泻火解毒，止血，安胎。用于湿温、暑湿，胸闷呕恶，湿热痞满，泻痢，黄疸，肺热咳嗽，高热烦渴，血热吐衄，痈肿疮毒，胎动不安。",
        "description": "本品为类圆形或不规则形薄片。外表皮黄棕色或棕褐色。切面黄棕色或黄绿色，具放射状纹理。",
        "season": "秋季",
        "similar_herbs": [
            "太子参"
        ]
    },
    {
        "id": 25,
        "name": "甘草",
        "english_name": "licorice",
        "image_path": "/images/picture/甘草.jpg",
        "properties": "甘，平。归心、肺、脾、胃经。",
        "effects": "补脾益气，清热解毒，祛痰止咳，缓急止痛，调和诸药。用于脾胃虚弱，倦怠乏力，心悸气短，咳嗽痰多，脘腹、四肢挛急疼痛，痈肿疮毒，缓解药物毒性、烈性。",
        "description": "本品呈类圆形或椭圆形的厚片。外表皮红棕色或灰棕色，具纵皱纹。切面略显纤维性，中心黄白色，有明显放射状纹理及形成层环。质坚实，具粉性。气微，味甜而特殊。",
        "season": "冬季",
        "similar_herbs": [
            "当归",
            "大血藤"
        ]
    },
    {
        "id": 26,
        "name": "山豆根",
        "english_name": "Sophora tonkinensis",
        "image_path": "/images/picture/山豆根.jpg",
        "properties": "苦，寒；有毒。归肺、胃经。",
        "effects": "清热解毒，消肿利咽。用于火毒蕴结，乳蛾喉痹，咽喉肿痛，齿龈肿痛，口舌生疮。",
        "description": "本品呈不规则的类圆形厚片。外表皮棕色至棕褐色。切面皮部浅棕色，木部淡黄色。有豆腥气，味极苦。",
        "season": "夏季",
        "similar_herbs": [
            "西洋参",
            "山豆根",
            "北豆根"
        ]
    }
    ]
  },

  // 显示详情模态框
  showDetail(e) {
    const herb = e.currentTarget.dataset.herb;
    this.setData({
      showModal: true,
      currentHerb: herb
    });
  },

  // 隐藏模态框
  hideModal() {
    this.setData({ showModal: false });
  },

  // 跳转至指定页码
  goToPage(e) {
    const page = e.currentTarget.dataset.page;
    this.setData({ currentPage: page });
    // 这里添加实际的分页加载逻辑
  },

  // 下一页
  goToNextPage() {
    if (this.data.currentPage < this.data.totalPages) {
      this.setData({ currentPage: this.data.currentPage + 1 });
    }
  }
});