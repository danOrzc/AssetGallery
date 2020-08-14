//Maya ASCII 2020 scene
//Name: OldGarage.ma
//Last modified: Tue, Aug 04, 2020 05:34:05 AM
//Codeset: 1252
requires maya "2020";
requires "mtoa" "4.0.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 18362)\n";
fileInfo "UUID" "89DC8D6A-4BC5-893E-6019-E39D0E390CCD";
createNode transform -n "warehouse";
	rename -uid "33CE67C2-422D-F4E9-178E-8899F8178BE2";
createNode mesh -n "warehouseShape" -p "warehouse";
	rename -uid "A363EA95-4501-B930-4F6A-079F356C2603";
	addAttr -ci true -sn "mso" -ln "miShadingSamplesOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "msh" -ln "miShadingSamples" -min 0 -smx 8 -at "float";
	addAttr -ci true -sn "mdo" -ln "miMaxDisplaceOverride" -min 0 -max 1 -at "bool";
	addAttr -ci true -sn "mmd" -ln "miMaxDisplace" -min 0 -smx 1 -at "float";
	setAttr -k off ".v";
	setAttr ".iog[0].og[0].gcl" -type "componentList" 1 "f[0:10]";
	setAttr ".vir" yes;
	setAttr ".vif" yes;
	setAttr ".uvst[0].uvsn" -type "string" "map1";
	setAttr -s 36 ".uvst[0].uvsp[0:35]" -type "float2" 0.99267 0.88803071
		 0.99267 0.90989012 0.99267 0.93174964 0.99266994 0.95360911 0.99266994 0.97546864
		 0.99266994 0.9973281 0.0055406094 0.88803071 0.0055406094 0.90989017 0.0055406094
		 0.9317497 0.005540669 0.95360911 0.0055406094 0.97546864 0.0055406094 0.99732804
		 0.0035867787 0.0034684837 0.68929297 0.0034685233 0.68929309 0.42006248 0.0035867691
		 0.42006251 0.70531923 0.39387321 0.7053194 0.0050443113 0.98863202 0.0050444528 0.9886319
		 0.39387321 0.69503778 0.65796685 0.69503778 0.0040065292 0.99112993 0.0040065292
		 0.99112993 0.65796685 0.7090562 0.39375043 0.70905536 0.0067753196 0.98557347 0.0067759752
		 0.98557377 0.39375067 0.34803694 0.42862087 0.68368208 0.42862087 0.68368208 0.76069236
		 0.34803694 0.87420619 0.0038302541 0.4286207 0.33947533 0.4286207 0.33947533 0.87420607
		 0.0038302541 0.76069224;
	setAttr ".cuvs" -type "string" "map1";
	setAttr ".dcc" -type "string" "Ambient+Diffuse";
	setAttr ".covm[0]"  0 1 1;
	setAttr ".cdvm[0]"  0 1 1;
	setAttr ".ugsdt" no;
	setAttr -s 18 ".pt[0:17]" -type "float3"  1.9627182 0.005783109 -3.443161 
		1.9996374 0.005783109 -3.4551563 1.9996374 0.005783109 -3.4939756 1.9627182 0.005783109 
		-3.505971 1.9399011 0.005783109 -3.4745655 1.9627182 -3.6040323 -3.443161 1.9996374 
		-3.6040323 -3.4551563 1.9996374 -3.6040323 -3.4939756 1.9627182 -3.6040323 -3.505971 
		1.9399011 -3.6040323 -3.4745655 7.5712843 0.005783109 -3.461937 1.9859784 0.005783109 
		-3.461937 7.5712843 -3.3875124 -3.461937 1.9859784 -3.3875124 -3.461937 7.5712843 
		-2.5230634 -0.90587616 1.9859784 -2.5230634 -0.90587616 7.5712843 0.005783109 -0.90587616 
		1.9859784 0.005783109 -0.90587616;
	setAttr -s 18 ".vt[0:17]"  -1.26449966 0 3.75247025 -1.31064856 0 3.76746488
		 -1.31064856 0 3.81598878 -1.26449966 0 3.8309834 -1.23597813 0 3.79172683 -1.26449966 4.5122695 3.75247025
		 -1.31064856 4.5122695 3.76746488 -1.31064856 4.5122695 3.81598878 -1.26449966 4.5122695 3.8309834
		 -1.23597813 4.5122695 3.79172683 -8.27520752 0 3.77594066 -1.29357481 0 3.77594066
		 -8.27520752 4.24161959 3.77594066 -1.29357481 4.24161959 3.77594066 -8.27520752 3.16105843 0.58086467
		 -1.29357481 3.16105843 0.58086467 -8.27520752 0 0.58086467 -1.29357481 0 0.58086467;
	setAttr -s 27 ".ed[0:26]"  0 1 0 1 2 0 2 3 0 3 4 0 4 0 0 5 6 0 6 7 0
		 7 8 0 8 9 0 9 5 0 0 5 1 1 6 1 2 7 1 3 8 1 4 9 1 10 11 0 12 13 0 14 15 0 16 17 0 10 12 0
		 11 13 0 12 14 0 13 15 0 14 16 0 15 17 0 16 10 0 17 11 0;
	setAttr -s 11 -ch 44 ".fc[0:10]" -type "polyFaces" 
		f 4 0 11 -6 -11
		mu 0 4 0 1 7 6
		f 4 1 12 -7 -12
		mu 0 4 1 2 8 7
		f 4 2 13 -8 -13
		mu 0 4 2 3 9 8
		f 4 3 14 -9 -14
		mu 0 4 3 4 10 9
		f 4 4 10 -10 -15
		mu 0 4 4 5 11 10
		f 4 15 20 -17 -20
		mu 0 4 12 13 14 15
		f 4 16 22 -18 -22
		mu 0 4 16 17 18 19
		f 4 17 24 -19 -24
		mu 0 4 20 21 22 23
		f 4 18 26 -16 -26
		mu 0 4 24 25 26 27
		f 4 -27 -25 -23 -21
		mu 0 4 28 29 30 31
		f 4 25 19 21 23
		mu 0 4 32 33 34 35;
	setAttr ".cd" -type "dataPolyComponent" Index_Data Edge 0 ;
	setAttr ".cvd" -type "dataPolyComponent" Index_Data Vertex 0 ;
	setAttr ".pd[0]" -type "dataPolyComponent" Index_Data UV 0 ;
	setAttr ".hfd" -type "dataPolyComponent" Index_Data Face 0 ;
	setAttr ".vnm" 0;
	setAttr ".ai_translator" -type "string" "polymesh";
createNode groupId -n "WAREHOUSE:groupId27";
	rename -uid "77218F1A-46CF-88F5-8CA4-E2ABB02FC4E6";
	setAttr ".ihi" 0;
createNode shadingEngine -n "WAREHOUSE:lambert2SG";
	rename -uid "495CC982-46DB-E8C4-E1C7-B0859744F286";
	setAttr ".ihi" 0;
	setAttr ".ro" yes;
createNode materialInfo -n "WAREHOUSE:materialInfo1";
	rename -uid "ED4C28E8-44EF-D0F8-8D76-F6BF355648DF";
createNode lambert -n "WAREHOUSE:FIRSTBUILDING";
	rename -uid "0C06685D-424B-F0EC-5183-4CAF5538B044";
createNode file -n "WAREHOUSE:file1";
	rename -uid "78DAD086-4880-B59A-EA29-64B31F2F0CE0";
	setAttr ".ftn" -type "string" "E:/Turbosquid/WAREHOUSE LOW POLY/MAYA FILE/WAREHOUSE.jpg";
	setAttr ".cs" -type "string" "sRGB";
createNode place2dTexture -n "WAREHOUSE:place2dTexture1";
	rename -uid "35373815-428B-E338-DC84-53BFC095BB91";
createNode lightLinker -s -n "lightLinker1";
	rename -uid "EC2003F8-4686-6DED-3F29-9D8F4FC9E9B3";
	setAttr -s 10 ".lnk";
	setAttr -s 10 ".slnk";
select -ne :time1;
	setAttr ".o" 1;
	setAttr ".unw" 1;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 22 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surface" "Particles" "Particle Instance" "Fluids" "Strokes" "Image Planes" "UI" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Hair Systems" "Follicles" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 22 0 1 1 1 1 1
		 1 1 1 0 0 0 0 0 0 0 0 0
		 0 0 0 0 ;
	setAttr ".fprt" yes;
select -ne :renderPartition;
	setAttr -s 10 ".st";
select -ne :renderGlobalsList1;
select -ne :defaultShaderList1;
	setAttr -s 13 ".s";
select -ne :postProcessList1;
	setAttr -s 2 ".p";
select -ne :defaultRenderUtilityList1;
	setAttr -s 11 ".u";
select -ne :defaultRenderingList1;
select -ne :defaultTextureList1;
	setAttr -s 10 ".tx";
select -ne :lambert1;
	setAttr ".c" -type "float3" 1 1 1 ;
select -ne :initialShadingGroup;
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr ".ro" yes;
select -ne :initialMaterialInfo;
select -ne :defaultRenderGlobals;
	addAttr -ci true -h true -sn "dss" -ln "defaultSurfaceShader" -dt "string";
	setAttr ".ren" -type "string" "arnold";
	setAttr ".outf" 8;
	setAttr ".dss" -type "string" "RoadRiverShader1";
select -ne :defaultResolution;
	setAttr ".pa" 1;
select -ne :hardwareRenderGlobals;
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
connectAttr "WAREHOUSE:groupId27.id" "warehouseShape.iog.og[0].gid";
connectAttr "WAREHOUSE:lambert2SG.mwc" "warehouseShape.iog.og[0].gco";
connectAttr "WAREHOUSE:FIRSTBUILDING.oc" "WAREHOUSE:lambert2SG.ss";
connectAttr "warehouseShape.iog.og[0]" "WAREHOUSE:lambert2SG.dsm" -na;
connectAttr "WAREHOUSE:groupId27.msg" "WAREHOUSE:lambert2SG.gn" -na;
connectAttr "WAREHOUSE:lambert2SG.msg" "WAREHOUSE:materialInfo1.sg";
connectAttr "WAREHOUSE:FIRSTBUILDING.msg" "WAREHOUSE:materialInfo1.m";
connectAttr "WAREHOUSE:file1.msg" "WAREHOUSE:materialInfo1.t" -na;
connectAttr "WAREHOUSE:file1.oc" "WAREHOUSE:FIRSTBUILDING.c";
connectAttr "WAREHOUSE:place2dTexture1.c" "WAREHOUSE:file1.c";
connectAttr "WAREHOUSE:place2dTexture1.tf" "WAREHOUSE:file1.tf";
connectAttr "WAREHOUSE:place2dTexture1.rf" "WAREHOUSE:file1.rf";
connectAttr "WAREHOUSE:place2dTexture1.mu" "WAREHOUSE:file1.mu";
connectAttr "WAREHOUSE:place2dTexture1.mv" "WAREHOUSE:file1.mv";
connectAttr "WAREHOUSE:place2dTexture1.s" "WAREHOUSE:file1.s";
connectAttr "WAREHOUSE:place2dTexture1.wu" "WAREHOUSE:file1.wu";
connectAttr "WAREHOUSE:place2dTexture1.wv" "WAREHOUSE:file1.wv";
connectAttr "WAREHOUSE:place2dTexture1.re" "WAREHOUSE:file1.re";
connectAttr "WAREHOUSE:place2dTexture1.of" "WAREHOUSE:file1.of";
connectAttr "WAREHOUSE:place2dTexture1.r" "WAREHOUSE:file1.ro";
connectAttr "WAREHOUSE:place2dTexture1.n" "WAREHOUSE:file1.n";
connectAttr "WAREHOUSE:place2dTexture1.vt1" "WAREHOUSE:file1.vt1";
connectAttr "WAREHOUSE:place2dTexture1.vt2" "WAREHOUSE:file1.vt2";
connectAttr "WAREHOUSE:place2dTexture1.vt3" "WAREHOUSE:file1.vt3";
connectAttr "WAREHOUSE:place2dTexture1.vc1" "WAREHOUSE:file1.vc1";
connectAttr "WAREHOUSE:place2dTexture1.o" "WAREHOUSE:file1.uv";
connectAttr "WAREHOUSE:place2dTexture1.ofs" "WAREHOUSE:file1.fs";
connectAttr ":defaultColorMgtGlobals.cme" "WAREHOUSE:file1.cme";
connectAttr ":defaultColorMgtGlobals.cfe" "WAREHOUSE:file1.cmcf";
connectAttr ":defaultColorMgtGlobals.cfp" "WAREHOUSE:file1.cmcp";
connectAttr ":defaultColorMgtGlobals.wsn" "WAREHOUSE:file1.ws";
relationship "link" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "link" ":lightLinker1" "WAREHOUSE:lambert2SG.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialShadingGroup.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" ":initialParticleSE.message" ":defaultLightSet.message";
relationship "shadowLink" ":lightLinker1" "WAREHOUSE:lambert2SG.message" ":defaultLightSet.message";
connectAttr "WAREHOUSE:lambert2SG.pa" ":renderPartition.st" -na;
connectAttr "WAREHOUSE:FIRSTBUILDING.msg" ":defaultShaderList1.s" -na;
connectAttr "WAREHOUSE:place2dTexture1.msg" ":defaultRenderUtilityList1.u" -na;
connectAttr "WAREHOUSE:file1.msg" ":defaultTextureList1.tx" -na;
// End of OldGarage.ma
