The following is the default log. It seems to load the armature just fine.

* add print statements to check how is the t-shape being added



```
Load and retarget /home/a9fb1e/github-work/human-renderer/makehuman_data/poses/cmu_motion_captures/01/01_06.bvh
Loading BVH file /home/a9fb1e/github-work/human-renderer/makehuman_data/poses/cmu_motion_captures/01/01_06.bvh (0 pct)
Reading skeleton
Reading motion
1000 (3.9 pct)
Bvh file /home/a9fb1e/github-work/human-renderer/makehuman_data/poses/cmu_motion_captures/01/01_06.bvh loaded in 1.280 s (100 pct)
File 01_06 5
Name Y_01_06
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/mh-alpha7.trg
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/mh-official.trg
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/rigify2.trg
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/genesis3.trg
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/rigify.trg
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/genesis.trg
Read target file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/target_rigs/mhx.trg
Defined McpTargetRig
Guessing target
  Try hips: Hips, children: 3
Mapping bones automatically:
  hips: Hips
  spine: LowerBack
  right leg: RHipJoint
  left leg: LHipJoint
  spine: LowerBack
  chest: Spine1
  shoulder.R: RightShoulder
  upper_arm.R: RightArm
  forearm.R: RightForeArm
  hand.R: RightHand
  neck: Neck
  shoulder.L: LeftShoulder
  upper_arm.L: LeftArm
  forearm.L: LeftForeArm
  hand.L: LeftHand
  hip.L: LHipJoint
  thigh.L: LeftUpLeg
  shin.L: LeftLeg
  foot.L: LeftFoot
  hip.R: RHipJoint
  thigh.R: RightUpLeg
  shin.R: RightLeg
  foot.R: RightFoot
Target Armature: Automatic
            hips           hips
       lowerback          spine
           spine        spine-1
          spine1          chest
   rightshoulder     shoulder.R
        rightarm    upper_arm.R
    rightforearm      forearm.R
       righthand         hand.R
            neck           neck
           neck1           head
    leftshoulder     shoulder.L
         leftarm    upper_arm.L
     leftforearm      forearm.L
        lefthand         hand.L
       lhipjoint          hip.L
       leftupleg        thigh.L
         leftleg         shin.L
        leftfoot         foot.L
     lefttoebase          toe.L
       rhipjoint          hip.R
      rightupleg        thigh.R
        rightleg         shin.R
       rightfoot         foot.R
    righttoebase          toe.R
Read source file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/source_rigs/eyes.src
Read source file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/source_rigs/accad.src
Read source file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/source_rigs/vicon.src
Read source file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/source_rigs/mb.src
Read source file /home/a9fb1e/opt/blender-2.80-6fd11a21f5c5-linux-glibc224-x86_64/2.80/scripts/addons/makewalk/source_rigs/max.src
Defined McpSourceRig
  Try hips: hip, children: 3
Mapping bones automatically:
  hips: hip
  spine: abdomen
  right leg: rButtock
  left leg: lButtock
  spine: abdomen
  chest: chest
  shoulder.R: rCollar
  upper_arm.R: rShldr
  forearm.R: rForeArm
  hand.R: rHand
  neck: neck
  shoulder.L: lCollar
  upper_arm.L: lShldr
  forearm.L: lForeArm
  hand.L: lHand
  hip.L: lButtock
  thigh.L: lThigh
  shin.L: lShin
  foot.L: lFoot
  hip.R: rButtock
  thigh.R: rThigh
  shin.R: rShin
  foot.R: rFoot
Auto T-pose Y_01_06
Source Armature: Automatic
             hip           hips
         abdomen          spine
           chest          chest
         rcollar     shoulder.R
          rshldr    upper_arm.R
        rforearm      forearm.R
           rhand         hand.R
            neck           neck
            head           head
         lcollar     shoulder.L
          lshldr    upper_arm.L
        lforearm      forearm.L
           lhand         hand.L
        lbuttock          hip.L
          lthigh        thigh.L
           lshin         shin.L
           lfoot         foot.L
        rbuttock          hip.R
          rthigh        thigh.R
           rshin         shin.R
           rfoot         foot.R
Using matching armature Automatic.
Rescale Y_01_06 with factor 0.016478
Retargeting (0 pct)
Set source armature to Automatic
Retarget Y_01_06 --> Testmodel_cmu_meter_foot
Guessing target
  Try hips: Hips, children: 3
Mapping bones automatically:
  hips: Hips
  spine: LowerBack
  right leg: RHipJoint
  left leg: LHipJoint
  spine: LowerBack
  chest: Spine1
  shoulder.R: RightShoulder
  upper_arm.R: RightArm
  forearm.R: RightForeArm
  hand.R: RightHand
  neck: Neck
  shoulder.L: LeftShoulder
  upper_arm.L: LeftArm
  forearm.L: LeftForeArm
  hand.L: LeftHand
  hip.L: LHipJoint
  thigh.L: LeftUpLeg
  shin.L: LeftLeg
  foot.L: LeftFoot
  hip.R: RHipJoint
  thigh.R: RightUpLeg
  shin.R: RightLeg
  foot.R: RightFoot
Target Armature: Automatic
            hips           hips
       lowerback          spine
           spine        spine-1
          spine1          chest
   rightshoulder     shoulder.R
        rightarm    upper_arm.R
    rightforearm      forearm.R
       righthand         hand.R
            neck           neck
           neck1           head
    leftshoulder     shoulder.L
         leftarm    upper_arm.L
     leftforearm      forearm.L
        lefthand         hand.L
       lhipjoint          hip.L
       leftupleg        thigh.L
         leftleg         shin.L
        leftfoot         foot.L
     lefttoebase          toe.L
       rhipjoint          hip.R
      rightupleg        thigh.R
        rightleg         shin.R
       rightfoot         foot.R
    righttoebase          toe.R
  - LeftToeBase toe.L
  - Spine spine-1
  - RightToeBase toe.R
Auto T-pose Testmodel_cmu_meter_foot
0 (0.0 pct)
100 (39.8 pct)
200 (79.7 pct)
Retargeted Y_01_06 --> Testmodel_cmu_meter_foot (100 pct)
Curves simplified
/home/a9fb1e/github-work/human-renderer/makehuman_data/poses/cmu_motion_captures/01/01_06.bvh finished in 4.862 s
```









And this is the log for a proper retargeting on 2.79:

```
Load and retarget /home/a9fb1e/Desktop/01_06.bvh
Loading BVH file /home/a9fb1e/Desktop/01_06.bvh (0 pct)
Reading skeleton
Reading motion
1000 (3.9 pct)
2000 (7.8 pct)
3000 (11.7 pct)
4000 (15.6 pct)
5000 (19.5 pct)
Bvh file /home/a9fb1e/Desktop/01_06.bvh loaded in 7.816 s (100 pct)
File 01_06 5
Name Y_01_06
Read target file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/target_rigs/default.trg
Read target file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/target_rigs/mb.trg
Read target file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/target_rigs/mh-alpha7.trg
Read target file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/target_rigs/rigify.trg
Read target file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/target_rigs/mhx.trg
Defined McpTargetRig
Guessing target
  Try hips: Hips, children: 3
Mapping bones automatically:
  hips: Hips
  spine: LowerBack
  right leg: RHipJoint
  left leg: LHipJoint
  spine: LowerBack
  chest: Spine1
  shoulder.R: RightShoulder
  upper_arm.R: RightArm
  forearm.R: RightForeArm
  hand.R: RightHand
  neck: Neck
  shoulder.L: LeftShoulder
  upper_arm.L: LeftArm
  forearm.L: LeftForeArm
  hand.L: LeftHand
  hip.L: LHipJoint
  thigh.L: LeftUpLeg
  shin.L: LeftLeg
  foot.L: LeftFoot
  hip.R: RHipJoint
  thigh.R: RightUpLeg
  shin.R: RightLeg
  foot.R: RightFoot
Target Armature: Automatic
            hips           hips
       lowerback          spine
           spine        spine-1
          spine1          chest
   rightshoulder     shoulder.R
        rightarm    upper_arm.R
    rightforearm      forearm.R
       righthand         hand.R
            neck           neck
           neck1           head
    leftshoulder     shoulder.L
         leftarm    upper_arm.L
     leftforearm      forearm.L
        lefthand         hand.L
       lhipjoint          hip.L
       leftupleg        thigh.L
         leftleg         shin.L
        leftfoot         foot.L
     lefttoebase          toe.L
       rhipjoint          hip.R
      rightupleg        thigh.R
        rightleg         shin.R
       rightfoot         foot.R
    righttoebase          toe.R
Read source file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/source_rigs/eyes.src
Read source file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/source_rigs/accad.src
Read source file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/source_rigs/vicon.src
Read source file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/source_rigs/mb.src
Read source file /home/a9fb1e/opt/blender-2.79b-linux-glibc219-x86_64/2.79/scripts/addons_contrib/makewalk/source_rigs/max.src
Defined McpSourceRig
  Try hips: hip, children: 3
Mapping bones automatically:
  hips: hip
  spine: abdomen
  right leg: rButtock
  left leg: lButtock
  spine: abdomen
  chest: chest
  shoulder.R: rCollar
  upper_arm.R: rShldr
  forearm.R: rForeArm
  hand.R: rHand
  neck: neck
  shoulder.L: lCollar
  upper_arm.L: lShldr
  forearm.L: lForeArm
  hand.L: lHand
  hip.L: lButtock
  thigh.L: lThigh
  shin.L: lShin
  foot.L: lFoot
  hip.R: rButtock
  thigh.R: rThigh
  shin.R: rShin
  foot.R: rFoot
Auto T-pose Y_01_06
Source Armature: Automatic
             hip           hips
         abdomen          spine
           chest          chest
         rcollar     shoulder.R
          rshldr    upper_arm.R
        rforearm      forearm.R
           rhand         hand.R
            neck           neck
            head           head
         lcollar     shoulder.L
          lshldr    upper_arm.L
        lforearm      forearm.L
           lhand         hand.L
        lbuttock          hip.L
          lthigh        thigh.L
           lshin         shin.L
           lfoot         foot.L
        rbuttock          hip.R
          rthigh        thigh.R
           rshin         shin.R
           rfoot         foot.R
Using matching armature Automatic.
Rescale Y_01_06 with factor 0.010711
Retargeting (0 pct)
Set source armature to Automatic
Retarget Y_01_06 --> Testmodel_cmu_meter
Guessing target
  Try hips: Hips, children: 3
Mapping bones automatically:
  hips: Hips
  spine: LowerBack
  right leg: RHipJoint
  left leg: LHipJoint
  spine: LowerBack
  chest: Spine1
  shoulder.R: RightShoulder
  upper_arm.R: RightArm
  forearm.R: RightForeArm
  hand.R: RightHand
  neck: Neck
  shoulder.L: LeftShoulder
  upper_arm.L: LeftArm
  forearm.L: LeftForeArm
  hand.L: LeftHand
  hip.L: LHipJoint
  thigh.L: LeftUpLeg
  shin.L: LeftLeg
  foot.L: LeftFoot
  hip.R: RHipJoint
  thigh.R: RightUpLeg
  shin.R: RightLeg
  foot.R: RightFoot
Target Armature: Automatic
            hips           hips
       lowerback          spine
           spine        spine-1
          spine1          chest
   rightshoulder     shoulder.R
        rightarm    upper_arm.R
    rightforearm      forearm.R
       righthand         hand.R
            neck           neck
           neck1           head
    leftshoulder     shoulder.L
         leftarm    upper_arm.L
     leftforearm      forearm.L
        lefthand         hand.L
       lhipjoint          hip.L
       leftupleg        thigh.L
         leftleg         shin.L
        leftfoot         foot.L
     lefttoebase          toe.L
       rhipjoint          hip.R
      rightupleg        thigh.R
        rightleg         shin.R
       rightfoot         foot.R
    righttoebase          toe.R
  - LeftToeBase toe.L
  - Spine spine-1
  - RightToeBase toe.R
0 (0.0 pct)
100 (10.0 pct)
200 (20.0 pct)
300 (30.0 pct)
400 (40.0 pct)
500 (50.0 pct)
600 (59.9 pct)
700 (69.9 pct)
800 (79.9 pct)
900 (89.9 pct)
1000 (99.9 pct)
Retargeted Y_01_06 --> Testmodel_cmu_meter (100 pct)
Curves simplified
/home/a9fb1e/Desktop/01_06.bvh finished in 21.166 s
```
