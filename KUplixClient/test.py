"""import os
import gi, time
import threading
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import Gst, GObject, Gtk, Gdk

class GTK_Main:
    def __init__(self):
        window = Gtk.Window(Gtk.WindowType.TOPLEVEL)
        window.set_title("Vorbis-Player")
        window.set_default_size(500, -1)
        window.connect("destroy", Gtk.main_quit, "WM destroy")
        vbox = Gtk.VBox()
        window.add(vbox)
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, False, 0)
        hbox = Gtk.HBox()
        vbox.add(hbox)
        buttonbox = Gtk.HButtonBox()
        hbox.pack_start(buttonbox, False, False, 0)
        rewind_button = Gtk.Button("Rewind")
        rewind_button.connect("clicked", self.rewind_callback)
        buttonbox.add(rewind_button)
        self.button = Gtk.Button("Start")
        self.button.connect("clicked", self.start_stop)
        buttonbox.add(self.button)
        forward_button = Gtk.Button("Forward")
        forward_button.connect("clicked", self.forward_callback)
        buttonbox.add(forward_button)
        self.time_label = Gtk.Label()
        self.time_label.set_text("00:00 / 00:00")
        hbox.add(self.time_label)
        window.show_all()

        self.player = Gst.Pipeline.new("player")
        source = Gst.ElementFactory.make("filesrc", "file-source")
        demuxer = Gst.ElementFactory.make("oggdemux", "demuxer")
        demuxer.connect("pad-added", self.demuxer_callback)
        self.audio_decoder = Gst.ElementFactory.make("vorbisdec", "vorbis-decoder")
        audioconv = Gst.ElementFactory.make("audioconvert", "converter")
        audiosink = Gst.ElementFactory.make("autoaudiosink", "audio-output")

        for ele in [source, demuxer, self.audio_decoder, audioconv, audiosink]:
            self.player.add(ele)
        source.link(demuxer)
        self.audio_decoder.link(audioconv)
        audioconv.link(audiosink)

        bus = self.player.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)

    def start_stop(self, w):
        if self.button.get_label() == "Start":
            filepath = self.entry.get_text().strip()
            if os.path.isfile(filepath):
                filepath = os.path.realpath(filepath)
                self.button.set_label("Stop")
                self.player.get_by_name("file-source").set_property("location", "udp://127.0.0.1:5005")
                self.player.set_state(Gst.State.PLAYING)
                self.play_thread_id = threading._start_new_thread(self.play_thread, ())
            else:
                self.play_thread_id = None
                self.player.set_state(Gst.State.NULL)
                self.button.set_label("Start")
                self.time_label.set_text("00:00 / 00:00")

    def play_thread(self):
        play_thread_id = self.play_thread_id
        Gdk.threads_enter()
        self.time_label.set_text("00:00 / 00:00")
        Gdk.threads_leave()

        while play_thread_id == self.play_thread_id:
            try:
                time.sleep(0.2)
                dur_int = self.player.query_duration(Gst.Format.TIME, None)[0]
                if dur_int == -1:
                    continue
                dur_str = self.convert_ns(dur_int)
                Gdk.threads_enter()
                self.time_label.set_text("00:00 / " + dur_str)
                Gdk.threads_leave()
                break
            except:
                pass

        time.sleep(0.2)
        while play_thread_id == self.play_thread_id:
            pos_int = self.player.query_position(Gst.Format.TIME, None)[0]
            pos_str = self.convert_ns(pos_int)
            if play_thread_id == self.play_thread_id:
                Gdk.threads_enter()
                self.time_label.set_text(pos_str + " / " + dur_str)
                Gdk.threads_leave()
            time.sleep(1)

    def on_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.EOS:
            self.play_thread_id = None
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            self.time_label.set_text("00:00 / 00:00")
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("Error: ", err, debug)
            self.play_thread_id = None
            self.player.set_state(Gst.State.NULL)
            self.button.set_label("Start")
            self.time_label.set_text("00:00 / 00:00")

    def demuxer_callback(self, demuxer, pad):
        adec_pad = self.audio_decoder.get_static_pad("sink")
        pad.link(adec_pad)

    def rewind_callback(self, w):
        rc, pos_int = self.player.query_position(Gst.Format.TIME)
        seek_ns = pos_int - 10 * 1000000000
        if seek_ns < 0:
            seek_ns = 0
        print('Backward:', pos_int,'ns -> ', seek_ns, 'ns')
        self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, seek_ns)

    def forward_callback(self, w):
        rc, pos_int = self.player.query_position(Gst.Format.TIME)
        seek_ns = pos_int + 10 * 1000000000
        print('Forward:', pos_int, 'ns -> ', seek_ns, 'ns')
        self.player.seek_simple(Gst.Format.TIME, Gst.SeekFlags.FLUSH, seek_ns)

    def convert_ns(self, t):
        # This method was submitted by Sam Mason.
        # It's much shorter than the original one.
        s,ns = divmod(t, 1000000000)
        m,s = divmod(s, 60)

        if m < 60:
            return "%02i:%02i" %(m,s)
        else:
            h,m = divmod(m, 60)
            return "%i:%02i:%02i" %(h,m,s)

GObject.threads_init()
Gst.init(None)
GTK_Main()
Gtk.main()


# !/usr/bin/python3

from os import path

import gi

gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

GObject.threads_init()
Gst.init(None)
#filename = path.join(path.dirname(path.abspath(__file__)), 'LiveStream.avi')
#uri = 'file://' + filename
uri = "udp://localhost:5005"

class Player(object):
    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(800, 450)

        self.drawingarea = Gtk.DrawingArea()
        self.window.add(self.drawingarea)
        
        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::eos', self.on_eos)
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        # Create GStreamer elements
        self.playbin = Gst.ElementFactory.make('playbin', None)

        # Add playbin to the pipeline
        self.pipeline.add(self.playbin)

        # Set properties
        self.playbin.set_property('uri', uri)

    def run(self):
        self.window.show_all()
        # You need to get the XID after window.show_all().  You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.drawingarea.get_property('window').get_xid()
        self.pipeline.set_state(Gst.State.PLAYING)
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_window_handle(self.xid)

    def on_eos(self, bus, msg):
        print('on_eos(): seeking to start of video')
        #self.playbin = Gst.ElementFactory.make('playbin', None)
        self.playbin.set_property('uri', uri)
        self.pipeline.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            0
        )

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())


p = Player()
p.run()
"""

#!/usr/bin/python3

# this example shows how to receive, decode and display a RTP h264 stream
# I'm using it to receive stream from Raspberry Pi
# This is the pipeline :
# gst-launch-1.0 -e -vvvv udpsrc port=5000 ! application/x-rtp, payload=96 ! rtpjitterbuffer ! rtph264depay ! avdec_h264 ! fpsdisplaysink sync=false text-overlay=false

import gi
gi.require_version('Gst', '1.0')
gi.require_version('Gtk', '3.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import GObject, Gst, Gtk

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

GObject.threads_init()
Gst.init(None)

class RTPStream:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect('destroy', self.quit)
        self.window.set_default_size(800, 450)

        self.drawingarea = Gtk.DrawingArea()
        self.window.add(self.drawingarea)

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline()

        # Create bus to get events from GStreamer pipeline
        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect('message::error', self.on_error)

        # This is needed to make the video output in our DrawingArea:
        self.bus.enable_sync_message_emission()
        self.bus.connect('sync-message::element', self.on_sync_message)

        # Create GStreamer elements
        self.udpsrc = Gst.ElementFactory.make('udpsrc', None)
        self.udpsrc.set_property('port', 5005)
        self.buffer = Gst.ElementFactory.make('rtpjitterbuffer',None)
        self.depay = Gst.ElementFactory.make('rtph264depay', None)
        self.decoder = Gst.ElementFactory.make('avdec_h264', None)
        self.sink = Gst.ElementFactory.make('autovideosink', None)

        # Add elements to the pipeline
        self.pipeline.add(self.udpsrc)
        self.pipeline.add(self.buffer)
        self.pipeline.add(self.depay)
        self.pipeline.add(self.decoder)
        self.pipeline.add(self.sink)

        self.udpsrc.link_filtered(self.depay, Gst.caps_from_string("application/x-rtp, payload=96"))
        self.depay.link(self.decoder)
        self.decoder.link(self.sink)

    def run(self):
        self.window.show_all()
        # You need to get the XID after window.show_all(). You shouldn't get it
        # in the on_sync_message() handler because threading issues will cause
        # segfaults there.
        self.xid = self.drawingarea.get_property('window').get_xid()
        self.pipeline.set_state(Gst.State.PLAYING)
        Gtk.main()

    def quit(self, window):
        self.pipeline.set_state(Gst.State.NULL)
        Gtk.main_quit()

    def on_sync_message(self, bus, msg):
        if msg.get_structure().get_name() == 'prepare-window-handle':
            print('prepare-window-handle')
            msg.src.set_property('force-aspect-ratio', True)
            msg.src.set_window_handle(self.xid)

    def on_error(self, bus, msg):
        print('on_error():', msg.parse_error())

rtpstream = RTPStream()
rtpstream.run()
