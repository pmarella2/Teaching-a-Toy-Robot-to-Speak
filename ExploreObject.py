#!/usr/bin/env python3

# Author: Praneeth Marella

import asyncio
import time
import sys
import os

import cozmo
from cozmo.util import degrees, distance_mm, speed_mmps, Pose, Angle
from cozmo.objects import LightCube, LightCube1Id, LightCube2Id, LightCube3Id

def handle_object_appeared(evt, **kw):
    # This will be called whenever an EvtObjectAppeared is dispatched -
    # whenever an Object comes into view.
    if isinstance(evt.obj, LightCube):
        print("Cozmo started seeing %s" % str(evt.obj.object_type))

def handle_object_disappeared(evt, **kw):
    # This will be called whenever an EvtObjectDisappeared is dispatched -
    # whenever an Object goes out of view.
    if isinstance(evt.obj, LightCube):
        print("Cozmo stopped seeing %s" % str(evt.obj.cube_id))

async def explore_sides(robot: cozmo.robot.Robot, found_cubes):
    await robot.turn_in_place(degrees(-45)).wait_for_completed()
    await robot.drive_straight(distance_mm(140), speed_mmps(200), False, False, 0).wait_for_completed()
    await robot.turn_in_place(degrees(75)).wait_for_completed()
    go_to_cube = robot.go_to_object(found_cubes[0], distance_mm(100.0))
    await go_to_cube.wait_for_completed()
    # await robot.drive_straight(distance_mm(140), speed_mmps(100), False, False, 0).wait_for_completed()
    await robot.drive_wheels(-200, -200, l_wheel_acc=4000, r_wheel_acc=4000, duration=1)

async def cozmo_program(robot: cozmo.robot.Robot):
    # Add event handlers for whenever Cozmo sees a new object
    robot.add_event_handler(cozmo.objects.EvtObjectAppeared, handle_object_appeared)
    robot.add_event_handler(cozmo.objects.EvtObjectDisappeared, handle_object_disappeared)

    # Connect to the pre-defined cubes
    await robot.world.connect_to_cubes()
    
    # Make sure Cozmo's head and arm are at reasonable levels
    await robot.set_head_angle(degrees(5.0)).wait_for_completed()
    await robot.set_lift_height(0.0).wait_for_completed()

    # Searches for the cubes for a defined time in seconds
    search_cubes = robot.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
    found_cubes = await robot.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=6)
    search_cubes.stop()

    found_cubes[0] = robot.world.get_light_cube(LightCube2Id)

    # Approach the object (pre-defined function used since its a defined object)
    go_to_cube = robot.go_to_object(found_cubes[0], distance_mm(100.0))
    await go_to_cube.wait_for_completed()
    # Code for objects that weren't pre-defined (we drive manually)
    # await robot.drive_straight(distance_mm(140), speed_mmps(100), False, False, 0).wait_for_completed()
    
    await robot.drive_wheels(-200, -200, l_wheel_acc=4000, r_wheel_acc=4000, duration=1)

    # Explore all sides of the object
    for sides in range(15):
        await explore_sides(robot, found_cubes)

    await robot.say_text("Exploration complete!").wait_for_completed()

    # Disconnects from the cubes
    robot.world.disconnect_from_cubes()

#cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_3d_viewer=True, use_viewer=True)
