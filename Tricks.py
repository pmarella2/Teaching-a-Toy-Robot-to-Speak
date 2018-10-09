#basic/learning Cozmo SDK code

#Cozmo will search for all three cubes
#if it does't find all three, it exits
#identified cubes light up in user (hard-coded) defined colors
#then it goes to a specified cube
#picks it up
#stacks it on top of a second defined cube
#then looks for third cube
#goes to the third cube
#then it pops a wheelie using its lift and cube
#drives backwards to get back into normal position
#does a victory dance

#Praneeth Marella

import asyncio
import sys
import time

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose, Angle
from cozmo.objects import LightCube1Id, LightCube2Id, LightCube3Id

async def cozmo_program(robot: cozmo.robot.Robot):
    #connects to the three pre-defined cubes
    await robot.world.connect_to_cubes()

    #(assuming starting point is the charger) moves off the charger then turns towards cubes
    await robot.drive_straight(distance_mm(100), speed_mmps(250)).wait_for_completed()
    await robot.turn_in_place(degrees(-45)).wait_for_completed()

    #searches for three cubes for 10 seconds
    search_cubes = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    found_cubes = await robot.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=10)
    search_cubes.stop()

    #checks to see if all three cubes are found - if they are, then we assign cubes
    if len(found_cubes) < 3:
        print("Need 3 cubes but found", len(found_cubes))
        sys.exit   
    else:
        found_cubes[0] = robot.world.get_light_cube(LightCube1Id)
        found_cubes[1] = robot.world.get_light_cube(LightCube2Id)
        found_cubes[2] = robot.world.get_light_cube(LightCube3Id)

    #lights up cubes in custom colors
    if found_cubes[0] is not None:
        found_cubes[0].set_light_corners(cozmo.lights.red_light, cozmo.lights.green_light, cozmo.lights.red_light, cozmo.lights.green_light)
    else:
        cozmo.logger.warning("Not connected to cube 1!")

    if found_cubes[1] is not None:
        found_cubes[1].set_light_corners(cozmo.lights.white_light, cozmo.lights.blue_light, cozmo.lights.white_light, cozmo.lights.blue_light)
    else:
        cozmo.logger.warning("Not connected to cube 2!")

    if found_cubes[2] is not None:
        found_cubes[2].set_lights(cozmo.lights.red_light)
    else:
        cozmo.logger.warning("Not connected to cube 3!")

    #goes to first cube
    go_to_cube = robot.go_to_object(found_cubes[0], distance_mm(70.0))
    await go_to_cube.wait_for_completed()

    #picks up the first cube within three tries - if it fails then a message is printed
    pick_up_cube = robot.pickup_object(found_cubes[0], num_retries=3)
    await pick_up_cube.wait_for_completed()
    if pick_up_cube.has_failed:
        code, reason = pick_up_cube.failure_reason
        result = pick_up_cube.result
        print("Picking up cube failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return

    #places the first cube on top of second cube once it reaches it - if it fails then a message is printed
    place_cube = robot.place_on_object(found_cubes[1], num_retries=3)
    await place_cube.wait_for_completed()
    if place_cube.has_failed:
        code, reason = place_cube.failure_reason
        result = place_cube.result
        print("Placing cube has failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return

    #does a wheelie on the third object once it reaches it - if it fails then a message is printed
    do_a_wheelie = robot.pop_a_wheelie(found_cubes[2], num_retries=2)
    await do_a_wheelie.wait_for_completed()
    if do_a_wheelie.has_failed:
        code, reason = do_a_wheelie.failure_reason
        result = do_a_wheelie.result
        print("Doing a wheelie has failed: code=%s reason='%s' result=%s" % (code, reason, result))
        return

    #drives backwards to get back into its regular position from the wheelie position
    await robot.drive_wheels(-200, -200, l_wheel_acc=4000, r_wheel_acc=4000, duration=0.6)
    #plays a victory dance to celebrate sucessful completeion
    await robot.play_anim_trigger(cozmo.anim.Triggers.CodeLabVictory).wait_for_completed()
    await robot.say_text("I did it!").wait_for_completed()

    #disconnects all three cubes
    robot.world.disconnect_from_cubes()

#opens a camera view and 3-d vector nav map of what cosmo sees
cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
