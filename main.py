#!/usr/bin/env python
""" qr scanner

https://www.simplifiedpython.net/kivy-button-example-tutorial-working-with-buttons-in-kivy/
"""

# W0613: Unused argument 'args' (unused-argument)
# pylint: disable=W0613


from kivy.app import App
#from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy_garden.zbarcam import ZBarCam

from jnius import autoclass


PythonActivity = autoclass('org.renpy.android.PythonActivity')
Intent = autoclass('android.content.Intent')
String = autoclass('java.lang.String')


class QrScanner(BoxLayout):
"""qr scanner class"""

    def __init__(self, **kwargs):
        """init reader"""
        super(QrScanner, self).__init__(**kwargs)
        btn1 = Button(text='Scan Me',  font_size="50sp")
        btn1.bind(on_press=self.callback) # pylint: disable=E1101
        self.add_widget(btn1)
        btn2 = Button(text='Share Me',  font_size="50sp")
        btn2.bind(on_press=self.share) # pylint: disable=E1101
        self.add_widget(btn2)
        self.zbarcam = None
        self.qr_text = None

    def callback(self, instance):
        """On click button, initiate zbarcam and schedule text reader"""
        self.remove_widget(instance) # remove button
        self.zbarcam = ZBarCam()
        self.add_widget(self.zbarcam)
        Clock.schedule_interval(self.read_qr_text, 1)

    def read_qr_text(self, *args):
        """Check if zbarcam.symbols is filled and stop scanning in such case"""
        if len(self.zbarcam.symbols) > 0: # when something is detected
            self.qr_text = self.zbarcam.symbols[0].data # text from QR
            Clock.unschedule(self.read_qr_text, 1)
            self.zbarcam.stop() # stop zbarcam
            # release camera
            self.zbarcam.ids['xcamera']._camera._device.release() # pylint: disable=W0212

    def share(self):
        """intent code"""
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String('test share text'))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String('Share...'))
        PythonActivity.mActivity.startActivity(chooser)

class QrApp(App):
    def build(self):
        """intent code"""
        return QrScanner()

if __name__ == '__main__':
    QrApp().run()
