//
//  support.m
//  xrecord
//
//  Created by Patrick Meenan on 2/24/15.
//  Copyright (c) 2015 WPO Foundation. All rights reserved.
//

#import "support.h"



BOOL signaled = NO;
int child_process = 0;

MyInterfaceStruct** interface;


static void signalHandler(int sig)
{
    signaled = YES;
    if (child_process != 0) {
        kill(child_process, sig);
    }
}

void onUncaughtException(NSException* exception)
{
    NSLog(@"uncaught exception: %@", exception.description);
}



@implementation XRecord_Bridge
- (void) startScreenCapturePlugin
{
    @autoreleasepool {
      interface = startScreenCapturePlugin();
    }
}

- (void) stopScreenCapturePlugin
{
    @autoreleasepool {
      stopScreenCapturePlugin(interface);
    }
}

- (void) enableScreenCaptureDevices
{
    // Enable iOS device to show up as AVCapture devices
    // From WWDC video 2014 #508 at 5:34
    // https://developer.apple.com/videos/wwdc/2014/#508
    CMIOObjectPropertyAddress prop = {
        kCMIOHardwarePropertyAllowScreenCaptureDevices,
        kCMIOObjectPropertyScopeGlobal,
        kCMIOObjectPropertyElementMaster };
    UInt32 allow = 1;
    CMIOObjectSetPropertyData(kCMIOObjectSystemObject, &prop, 0, NULL, sizeof(allow), &allow);
}

- (void) installSignalHandler:(int)child_pid
{
    child_process = child_pid;
    NSSetUncaughtExceptionHandler(&onUncaughtException);
    signal(SIGINT, signalHandler);
    signal(SIGTERM, signalHandler);
    signal(SIGQUIT, signalHandler);
    signal(SIGABRT, signalHandler);
}

- (BOOL) didSignal
{
    return signaled;
}

@end