from sshkeyboard import listen_keyboard, stop_listening

def press(key):
    print(f"Key pressed: {key}")

def release(key):
    print(f"Key released: {key}")

print("Listening to keybord input (over SSH). Press \"space\" to toggle, and \"ESC\" or \"q\" to quit")

listen_keyboard(
  on_press=press,
)