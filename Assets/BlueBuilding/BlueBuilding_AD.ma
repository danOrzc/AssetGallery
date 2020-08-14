//Maya ASCII 2020 scene
//Name: BlueBuilding_AD.ma
//Last modified: Tue, Aug 04, 2020 05:33:36 AM
//Codeset: 1252
requires maya "2020";
requires "mtoa" "4.0.0";
requires -nodeType "assemblyDefinition" "sceneAssembly" "1.0";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2020";
fileInfo "version" "2020";
fileInfo "cutIdentifier" "201911140446-42a737a01c";
fileInfo "osv" "Microsoft Windows 10 Technical Preview  (Build 18362)\n";
fileInfo "UUID" "7C15893A-49DE-130A-F20D-20B68C833FA3";
createNode assemblyDefinition -n "BlueBuildingAssembly";
	rename -uid "3071A590-4DB0-E7F8-0A19-D8B2EA6F885F";
	setAttr ".isc" yes;
	setAttr ".icn" -type "string" "out_assemblyDefinition.png";
	setAttr ".ctor" -type "string" "dog_d";
	setAttr ".cdat" -type "string" "2020/08/04 05:33:35";
	setAttr -s 3 ".rep";
	setAttr ".rep[0].rna" -type "string" "myLocator";
	setAttr ".rep[0].rla" -type "string" "Locator";
	setAttr ".rep[0].rty" -type "string" "Locator";
	setAttr ".rep[0].rda" -type "string" "Annotation: BlueBuildingAssembly";
	setAttr ".rep[1].rna" -type "string" "myScene";
	setAttr ".rep[1].rla" -type "string" "BlueBuilding.ma";
	setAttr ".rep[1].rty" -type "string" "Scene";
	setAttr ".rep[1].rda" -type "string" "C:/Users/dog_d/Desktop/AssetGallery/Assets/BlueBuilding/BlueBuilding.ma";
	setAttr ".rep[2].rna" -type "string" "myCache";
	setAttr ".rep[2].rla" -type "string" "BlueBuilding.abc";
	setAttr ".rep[2].rty" -type "string" "Cache";
	setAttr ".rep[2].rda" -type "string" "C:/Users/dog_d/Desktop/AssetGallery/Assets/BlueBuilding/BlueBuilding.abc";
createNode hyperLayout -n "hyperLayout1";
	rename -uid "AF3E0D1D-4166-174A-B751-AEA47D6B7C6B";
	setAttr ".ihi" 0;
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
connectAttr "hyperLayout1.msg" "BlueBuildingAssembly.hl";
// End of BlueBuilding_AD.ma
