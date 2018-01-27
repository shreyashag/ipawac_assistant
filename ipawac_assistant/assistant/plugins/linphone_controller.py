#!/usr/bin/env python

import linphone
import logging
import signal
import time
import jasperpath
import threading
import time


class SecurityCamera:
    def __init__(
            self,
            username='',
            password='',
            whitelist=[],
            camera='',
            snd_capture='',
            snd_playback=''):
        self.quit = False
        self.whitelist = whitelist
        callbacks = {
            'call_state_changed': self.call_state_changed,
        }

        # Configure the linphone core
        logging.basicConfig(level=logging.INFO)
        signal.signal(signal.SIGINT, self.signal_handler)
        # linphone.set_log_handler(self.log_handler)
        self.core = linphone.Core.new(callbacks, None, None)
        self.core.max_calls = 1
        self.core.echo_cancellation_enabled = False
        self.core.video_capture_enabled = True
        self.core.video_display_enabled = False
        self.core.stun_server = 'stun.linphone.org'
        self.core.ring = "../static/audio/telephone-ring-04.wav"
        self.core.ringback = jasperpath.data('audio', 'phone_ringing.wav')
        self.core.root_ca = "/usr/local/etc/openssl/cert.pem"
        # self.core.ice_enabled = True
        if len(camera):
            self.core.video_device = camera
        if len(snd_capture):
            self.core.capture_device = snd_capture
        if len(snd_playback):
            self.core.playback_device = snd_playback

        # Only enable PCMU and PCMA audio codecs
        # for codec in self.core.audio_codecs:
        #   if codec.mime_type == "PCMA" or codec.mime_type == "PCMU":
        #     self.core.enable_payload_type(codec, True)
        #   else:
        #     self.core.enable_payload_type(codec, False)

        # Only enable VP8 video codec
        for codec in self.core.video_codecs:
            if codec.mime_type == "VP8":
                self.core.enable_payload_type(codec, True)
            if codec.mime_type == "VP8":
                self.core.enable_payload_type(codec, True)
                # profile-level-id=42801F
        #   else:
        #     self.core.enable_payload_type(codec, False)

        self.configure_sip_account(username, password)

    def signal_handler(self, signal, frame):
        self.core.terminate_all_calls()
        self.quit = True

    def log_handler(self, level, msg):
        method = getattr(logging, level)
        method(msg)

    def call_state_changed(self, core, call, state, message):
        if state == linphone.CallState.IncomingReceived:
            if call.remote_address.as_string_uri_only() in self.whitelist:
                params = core.create_call_params(call)
                core.accept_call_with_params(call, params)
                chat_room = core.get_chat_room_from_uri(self.whitelist[0])
                msg = chat_room.create_message(
                    call.remote_address_as_string + ' tried to call')
                chat_room.send_chat_message(msg)
            else:
                core.decline_call(call, linphone.Reason.Declined)
                chat_room = core.get_chat_room_from_uri(self.whitelist[0])
                msg = chat_room.create_message(
                    call.remote_address_as_string + ' tried to call')
                chat_room.send_chat_message(msg)
        # if state == linphone.CallState.End:
        #   self.quit = True

    def configure_sip_account(self, username, password):
        # Configure the SIP account
        proxy_cfg = self.core.create_proxy_config()
        proxy_cfg.identity_address = self.core.create_address(
            'sip:{username}@sip.linphone.org'.format(username=username))
        proxy_cfg.server_addr = 'sip:sip.linphone.org;transport=tls'
        proxy_cfg.register_enabled = True
        self.core.add_proxy_config(proxy_cfg)
        auth_info = self.core.create_auth_info(
            username, None, password, None, None, 'sip.linphone.org')
        self.core.add_auth_info(auth_info)

    def create_call(self, personToCall):
        params = self.core.create_call_params(None)
        params.video_enabled = True
        personToCall = personToCall + '@sip.linphone.org'

        def make_call_thread(self, personToCall, params):
            print("Created a Call Thread!")
            mycall = self.core.invite_with_params(personToCall, params)

        call_thread = threading.Thread(
            target=make_call_thread, args=(
                self, personToCall, params))
        call_thread.daemon = True
        call_thread.start()
        print("Call thread started, enter \"End Call\" to end the call")

    def end_call(self):
        self.core.terminate_all_calls()

    def run(self):
        while not self.quit:
            self.core.iterate()
            time.sleep(0.03)


# def main():
#   cam= SecurityCamera(username='pi-shrex', password='school',
#    whitelist=['sip:shreyash23@sip.linphone.org', 'sip:nikhil93@sip.linphone.org','sip:amansalehjee@sip.linphone.org'],
# camera='Webcam QT Capture: FaceTime HD Camera (Built-in)',
# snd_capture='AudioUnit: Built-in Microphone
# (AppleHDAEngineInput:1B,0,1,0:1)',snd_playback='AudioUnit: Built-in
# Output (AppleHDAEngineOutput:1B,0,1,1:0)')

#   # obj=linphone.Core.video_devices
#   # print dict([attr, getattr(obj, attr)] for attr in dir(obj) if not attr.startswith('_'))
#   # pprint (dir(obj))
#   # print obj
#   # i=str(strings.__str__())
#   # print i
#   cam.run()
#   cam.create_call('shreyash23')

# main()
