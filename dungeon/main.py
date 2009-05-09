#
# This base-project contains all you need in order to set up an application
# with buffered event handling, without the need of SampleFramework or
# ExampleFrameListener classes. 
# It is based partially on Basic Tutorial 6 and bits from the SF.
#
# As an added bonus, I have added the code required for using CEGUI.
# It is the same as can be found in the basic tutorials.
#
# This code is public domain, feel free to do with it as you please
# 
# Alex de Landgraaf, 2008
#

import ogre.renderer.OGRE as ogre
import ogre.io.OIS as OIS
import ogre.gui.CEGUI as CEGUI

class EventListener(ogre.FrameListener, ogre.WindowEventListener, OIS.MouseListener, OIS.KeyListener, OIS.JoyStickListener):
    """
    This class handles all our ogre and OIS events, mouse/keyboard/joystick
    depending on how you initialize this class. All events are handled
    using callbacks (buffered).
    """
    
    mouse = None
    keyboard = None
    joy = None
    
    def __init__(self, renderWindow, bufferedMouse, bufferedKeys, bufferedJoy):
        
        # Initialize the various listener classes we are a subclass from
        ogre.FrameListener.__init__(self)
        ogre.WindowEventListener.__init__(self)
        OIS.MouseListener.__init__(self)
        OIS.KeyListener.__init__(self)
        OIS.JoyStickListener.__init__(self)

        self.renderWindow = renderWindow
        
        # Create the inputManager using the supplied renderWindow
        windowHnd = self.renderWindow.getCustomAttributeInt("WINDOW")
        self.inputManager = OIS.createPythonInputSystem([("WINDOW",str(windowHnd))])
        
        # Attempt to get the mouse/keyboard input objects,
        # and use this same class for handling the callback functions.
        # These functions are defined later on.
        
        try:
            if bufferedMouse:
                self.mouse = self.inputManager.createInputObjectMouse(OIS.OISMouse, bufferedMouse)
                self.mouse.setEventCallback(self)
                
            if bufferedKeys:
                self.keyboard = self.inputManager.createInputObjectKeyboard(OIS.OISKeyboard, bufferedKeys)
                self.keyboard.setEventCallback(self)
                
            if bufferedJoy:
                self.joy = self.inputManager.createInputObjectJoyStick(OIS.OISJoyStick, bufferedJoy)
                self.joy.setEventCallback(self)
                
        except Exception, e: # Unable to obtain mouse/keyboard/joy input
            raise e
        
        # Set this to True when we get an event to exit the application
        self.quitApplication = False
        
        # Listen for any events directed to the window manager's close button
        ogre.WindowEventUtilities.addWindowEventListener(self.renderWindow, self)
        
    def __del__ (self ):
        # Clean up OIS 
        print "QUITING"
        self.delInputObjects()

        del self.inputManager 
        
        self.windowClosed(self.renderWindow)
        
    def delInputObjects(self):
        # Clean up the initialized input objects
        if self.keyboard:
            self.inputManager.destroyInputObjectKeyboard(self.keyboard)
        if self.mouse:
            self.inputManager.destroyInputObjectMouse(self.mouse)
        if self.joy:
            self.inputManager.destroyInputObjectJoyStick(self.joy)
            
    def frameStarted(self, evt):
        """ 
        Called before a frame is displayed, handles events
        (also those via callback functions, as you need to call capture()
        on the input objects)
        
        Returning False here exits the application (render loop stops)
        """
        
        # Capture any buffered events and call any required callback functions
        if self.keyboard:
            self.keyboard.capture()
        if self.mouse:
            self.mouse.capture()
        if self.joy:
            self.joy.capture()
            
            # joystick test
            axes_int = self.joy.getJoyStickState().mAxes
            axes = []
            for i in axes_int:
                axes.append(i.abs)          
            print axes
            
        # Neatly close our FrameListener if our renderWindow has been shut down
        if(self.renderWindow.isClosed()):
            return False
        
        return not self.quitApplication
    
### Window Event Listener callbacks ###
    
    def windowResized(self, renderWindow):
        pass
    
    def windowClosed(self, renderWindow):
        # Only close for window that created OIS
        if(renderWindow == self.renderWindow):
            del self
            
### Mouse Listener callbacks ###
            
    def mouseMoved(self, evt):
        # Pass the location of the mouse pointer over to CEGUI
        CEGUI.System.getSingleton().injectMouseMove(evt.get_state().X.rel, evt.get_state().Y.rel)
        return True
    
    def mousePressed(self, evt, id):
        # Handle any CEGUI mouseButton events
        CEGUI.System.getSingleton().injectMouseButtonDown(self.convertButton(id))
        return True
    
    def mouseReleased(self, evt, id):
        # Handle any CEGUI mouseButton events
        CEGUI.System.getSingleton().injectMouseButtonUp(self.convertButton(id))
        return True
    
    
    def convertButton(self,oisID):
        if oisID == OIS.MB_Left:
            return CEGUI.LeftButton
        elif oisID == OIS.MB_Right:
            return CEGUI.RightButton
        elif oisID == OIS.MB_Middle:
            return CEGUI.MiddleButton
        else:
            return CEGUI.LeftButton     
        
### Key Listener callbacks ###
        
    def keyPressed(self, evt):
        # Quit the application if we hit the escape button
        if evt.key == OIS.KC_ESCAPE:
            self.quitApplication = True
            
            if evt.key == OIS.KC_1:
                print "hello"
                
        return True
    
    def keyReleased(self, evt):
        return True
    
### Joystick Listener callbacks ###
    
    def buttonPressed(self, evt, id):
        return True
    
    def buttonReleased(self, evt, id):
        return True
    
    def axisMoved(self, evt, id):
        return True
    
class Application(object):
    
    app_title = "MyApplication"
    
    def go(self):
        # See Basic Tutorial 6 for details
        self.createRoot()
        self.defineResources()
        self.setupRenderSystem()
        self.createRenderWindow()
        self.initializeResourceGroups()
        self.setupScene()
        self.createFrameListener()
        self.setupCEGUI()
        self.startRenderLoop()
        #self.cleanUp()
        
    def createRoot(self):
        self.root = ogre.Root()
        
    def defineResources(self):
        # Read the resources.cfg file and add all resource locations in it
        cf = ogre.ConfigFile()
        cf.load("resources.cfg")
        seci = cf.getSectionIterator()
        while seci.hasMoreElements():
            secName = seci.peekNextKey()
            settings = seci.getNext()
            for item in settings:
                typeName = item.key
                archName = item.value
                ogre.ResourceGroupManager.getSingleton().addResourceLocation(archName, typeName, secName)
                
                
    def setupRenderSystem(self):
        # Show the config dialog if we don't yet have an ogre.cfg file
        if not self.root.restoreConfig() and not self.root.showConfigDialog():
            raise Exception("User canceled config dialog! (setupRenderSystem)")
        
    def createRenderWindow(self):
        self.root.initialise(True, self.app_title)
        
    def initializeResourceGroups(self):
        ogre.TextureManager.getSingleton().setDefaultNumMipmaps(5)
        ogre.ResourceGroupManager.getSingleton().initialiseAllResourceGroups()
        
    def setupScene(self):
        self.renderWindow = self.root.getAutoCreatedWindow()
        self.sceneManager = self.root.createSceneManager(ogre.ST_GENERIC, "Default SceneManager")
        self.camera = self.sceneManager.createCamera("Camera")
        viewPort = self.root.getAutoCreatedWindow().addViewport(self.camera)
        
        self.camera.setPosition(ogre.Vector3(0, 100, -400))
        self.camera.lookAt(ogre.Vector3(0, 0, 1))
        
        
        self.sceneManager.setAmbientLight(ogre.ColourValue(0.7,0.7,0.7))
        self.sceneManager.setSkyDome(True, 'Examples/CloudySky',4, 8)
        self.sceneManager.setFog( ogre.FOG_EXP, ogre.ColourValue(1,1,1),0.0002)
        self.light = self.sceneManager.createLight( 'lightMain')
        self.light.setPosition ( ogre.Vector3(20, 80, 50) )
        
        self.rn = self.sceneManager.getRootSceneNode()
        
        self.entityOgre = self.sceneManager.createEntity('Ogre','ogrehead.mesh')
        self.nodeOgre = self.rn.createChildSceneNode('nodeOgre')
        self.nodeOgre.setPosition(ogre.Vector3(0, 0, 0))
        self.nodeOgre.attachObject(self.entityOgre)
        
        
    def createFrameListener(self):
        self.eventListener = EventListener(self.renderWindow, True, True, False) # switch the final "False" into "True" to get joystick support
        self.root.addFrameListener(self.eventListener)
        
    def setupCEGUI(self):
        sceneManager = self.sceneManager
        
        # CEGUI
        self.renderer = CEGUI.OgreCEGUIRenderer(self.renderWindow, ogre.RENDER_QUEUE_OVERLAY, False, 3000, sceneManager)
        self.system = CEGUI.System(self.renderer)
        
        CEGUI.SchemeManager.getSingleton().loadScheme("TaharezLookSkin.scheme")
        self.system.setDefaultMouseCursor("TaharezLook", "MouseArrow")
        self.system.setDefaultFont("BlueHighway-12")
        
        # Uncomment the following to read in a CEGUI sheet (from CELayoutEditor)
        # 
        # self.mainSheet = CEGUI.WindowManager.getSingleton().loadWindowLayout("myapplication.layout")
        # self.system.setGUISheet(self.mainSheet)
        
    def startRenderLoop(self):
        self.root.startRendering()
        
    def cleanUp(self):
        # Clean up CEGUI
        print "CLEANING"
        #del self.renderer
        del self.system
        
        # Clean up Ogre
        #del self.exitListener
        del self.root
        
        
if __name__ == '__main__':
    try:
        ta = Application()
        ta.go()
    except ogre.OgreException, e:
        print e
