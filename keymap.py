# ------------------------------------------------------------------
# keymap.py
# 
# string->key and key->string maps
# ------------------------------------------------------------------

import pygame

#  
#  Key String  Common Name
#
#  backspace   backspace
#  tab         tab
#  clear       clear
#  return      return
#  pause       pause
#  escape      escape
#  space       space
#  exclaim     exclaim
#  quotedbl    quotedbl
#  hash        hash
#  dollar      dollar
#  ampersand   ampersand
#  quote       quote
#  leftparen   left parenthesis
#  rightparen  right parenthesis
#  asterisk    asterisk
#  plus        plus sign
#  comma       comma
#  minus       minus sign
#  period      period
#  slash       forward slash
#  0           0
#  1           1
#  2           2
#  3           3
#  4           4
#  5           5
#  6           6
#  7           7
#  8           8
#  9           9
#  colon       colon
#  semicolon   semicolon
#  less        less-than sign
#  equals      equals sign
#  greater     greater-than sign
#  question    question mark
#  at          at
#  leftbracket left bracket
#  backslash   backslash
#  rightbracketright bracket
#  caret       caret
#  underscore  underscore
#  backquote   grave
#  a           a
#  b           b
#  c           c
#  d           d
#  e           e
#  f           f
#  g           g
#  h           h
#  i           i
#  j           j
#  k           k
#  l           l
#  m           m
#  n           n
#  o           o
#  p           p
#  q           q
#  r           r
#  s           s
#  t           t
#  u           u
#  v           v
#  w           w
#  x           x
#  y           y
#  z           z
#  delete      delete
#  kp0         keypad 0
#  kp1         keypad 1
#  kp2         keypad 2
#  kp3         keypad 3
#  kp4         keypad 4
#  kp5         keypad 5
#  kp6         keypad 6
#  kp7         keypad 7
#  kp8         keypad 8
#  kp9         keypad 9
#  kp_period   keypad period
#  kp_divide   keypad divide
#  kp_multiply keypad multiply
#  kp_minus    keypad minus
#  kp_plus     keypad plus
#  kp_enter    keypad enter
#  kp_equals   keypad equals
#  up          up arrow
#  down        down arrow
#  right       right arrow
#  left        left arrow
#  insert      insert
#  home        home
#  end         end
#  pageup      page up
#  pagedown    page down
#  f1          F1
#  f2          F2
#  f3          F3
#  f4          F4
#  f5          F5
#  f6          F6
#  f7          F7
#  f8          F8
#  f9          F9
#  f10         F10
#  f11         F11
#  f12         F12
#  f13         F13
#  f14         F14
#  f15         F15
#  numlock     numlock
#  capslock    capslock
#  scrollock   scrollock
#  rshift      right shift
#  lshift      left shift
#  rctrl       right ctrl
#  lctrl       left ctrl
#  ralt        right alt
#  lalt        left alt
#  rmeta       right meta
#  lmeta       left meta
#  lsuper      left windows key
#  rsuper      right windows key
#  mode        mode shift
#  help        help
#  print       print screen
#  sysreq      sysrq
#  break       break
#  menu        menu
#  power       power
#  euro        euro
#

str_to_key = {
    'backspace': pygame.K_BACKSPACE,
    'tab': pygame.K_TAB,
    'clear': pygame.K_CLEAR,
    'return': pygame.K_RETURN,
    'pause': pygame.K_PAUSE,
    'escape': pygame.K_ESCAPE,
    'space': pygame.K_SPACE,
    'exclaim': pygame.K_EXCLAIM,
    'quotedbl': pygame.K_QUOTEDBL,
    'hash': pygame.K_HASH,
    'dollar': pygame.K_DOLLAR,
    'ampersand': pygame.K_AMPERSAND,
    'quote': pygame.K_QUOTE,
    'leftparen': pygame.K_LEFTPAREN,
    'rightparen': pygame.K_RIGHTPAREN,
    'asterisk': pygame.K_ASTERISK,
    'plus': pygame.K_PLUS,
    'comma': pygame.K_COMMA,
    'minus': pygame.K_MINUS,
    'period': pygame.K_PERIOD,
    'slash': pygame.K_SLASH,
    '0': pygame.K_0,
    '1': pygame.K_1,
    '2': pygame.K_2,
    '3': pygame.K_3,
    '4': pygame.K_4,
    '5': pygame.K_5,
    '6': pygame.K_6,
    '7': pygame.K_7,
    '8': pygame.K_8,
    '9': pygame.K_9,
    'colon': pygame.K_COLON,
    'semicolon': pygame.K_SEMICOLON,
    'less': pygame.K_LESS,
    'equals': pygame.K_EQUALS,
    'greater': pygame.K_GREATER,
    'question': pygame.K_QUESTION,
    'at': pygame.K_AT,
    'leftbracket': pygame.K_LEFTBRACKET,
    'backslash': pygame.K_BACKSLASH,
    'rightbracket': pygame.K_RIGHTBRACKET,
    'caret': pygame.K_CARET,
    'underscore': pygame.K_UNDERSCORE,
    'backquote': pygame.K_BACKQUOTE,
    'a': pygame.K_a,
    'b': pygame.K_b,
    'c': pygame.K_c,
    'd': pygame.K_d,
    'e': pygame.K_e,
    'f': pygame.K_f,
    'g': pygame.K_g,
    'h': pygame.K_h,
    'i': pygame.K_i,
    'j': pygame.K_j,
    'k': pygame.K_k,
    'l': pygame.K_l,
    'm': pygame.K_m,
    'n': pygame.K_n,
    'o': pygame.K_o,
    'p': pygame.K_p,
    'q': pygame.K_q,
    'r': pygame.K_r,
    's': pygame.K_s,
    't': pygame.K_t,
    'u': pygame.K_u,
    'v': pygame.K_v,
    'w': pygame.K_w,
    'x': pygame.K_x,
    'y': pygame.K_y,
    'z': pygame.K_z,
    'delete': pygame.K_DELETE,
    'kp0': pygame.K_KP0,
    'kp1': pygame.K_KP1,
    'kp2': pygame.K_KP2,
    'kp3': pygame.K_KP3,
    'kp4': pygame.K_KP4,
    'kp5': pygame.K_KP5,
    'kp6': pygame.K_KP6,
    'kp7': pygame.K_KP7,
    'kp8': pygame.K_KP8,
    'kp9': pygame.K_KP9,
    'kp_period': pygame.K_KP_PERIOD,
    'kp_divide': pygame.K_KP_DIVIDE,
    'kp_multiply': pygame.K_KP_MULTIPLY,
    'kp_minus': pygame.K_KP_MINUS,
    'kp_plus': pygame.K_KP_PLUS,
    'kp_enter': pygame.K_KP_ENTER,
    'kp_equals': pygame.K_KP_EQUALS,
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'right': pygame.K_RIGHT,
    'left': pygame.K_LEFT,
    'insert': pygame.K_INSERT,
    'home': pygame.K_HOME,
    'end': pygame.K_END,
    'pageup': pygame.K_PAGEUP,
    'pagedown': pygame.K_PAGEDOWN,
    'f1': pygame.K_F1,
    'f2': pygame.K_F2,
    'f3': pygame.K_F3,
    'f4': pygame.K_F4,
    'f5': pygame.K_F5,
    'f6': pygame.K_F6,
    'f7': pygame.K_F7,
    'f8': pygame.K_F8,
    'f9': pygame.K_F9,
    'f10': pygame.K_F10,
    'f11': pygame.K_F11,
    'f12': pygame.K_F12,
    'f13': pygame.K_F13,
    'f14': pygame.K_F14,
    'f15': pygame.K_F15,
    'numlock': pygame.K_NUMLOCK,
    'capslock': pygame.K_CAPSLOCK,
    'scrollock': pygame.K_SCROLLOCK,
    'rshift': pygame.K_RSHIFT,
    'lshift': pygame.K_LSHIFT,
    'rctrl': pygame.K_RCTRL,
    'lctrl': pygame.K_LCTRL,
    'ralt': pygame.K_RALT,
    'lalt': pygame.K_LALT,
    'rmeta': pygame.K_RMETA,
    'lmeta': pygame.K_LMETA,
    'lsuper': pygame.K_LSUPER,
    'rsuper': pygame.K_RSUPER,
    'mode': pygame.K_MODE,
    'help': pygame.K_HELP,
    'print': pygame.K_PRINT,
    'sysreq': pygame.K_SYSREQ,
    'break': pygame.K_BREAK,
    'menu': pygame.K_MENU,
    'power': pygame.K_POWER,
    'euro': pygame.K_EURO,
}

key_to_str = {
    pygame.K_BACKSPACE: 'backspace',
    pygame.K_TAB: 'tab',
    pygame.K_CLEAR: 'clear',
    pygame.K_RETURN: 'return',
    pygame.K_PAUSE: 'pause',
    pygame.K_ESCAPE: 'escape',
    pygame.K_SPACE: 'space',
    pygame.K_EXCLAIM: 'exclaim',
    pygame.K_QUOTEDBL: 'quotedbl',
    pygame.K_HASH: 'hash',
    pygame.K_DOLLAR: 'dollar',
    pygame.K_AMPERSAND: 'ampersand',
    pygame.K_QUOTE: 'quote',
    pygame.K_LEFTPAREN: 'leftparen',
    pygame.K_RIGHTPAREN: 'rightparen',
    pygame.K_ASTERISK: 'asterisk',
    pygame.K_PLUS: 'plus',
    pygame.K_COMMA: 'comma',
    pygame.K_MINUS: 'minus',
    pygame.K_PERIOD: 'period',
    pygame.K_SLASH: 'slash',
    pygame.K_0: '0',
    pygame.K_1: '1',
    pygame.K_2: '2',
    pygame.K_3: '3',
    pygame.K_4: '4',
    pygame.K_5: '5',
    pygame.K_6: '6',
    pygame.K_7: '7',
    pygame.K_8: '8',
    pygame.K_9: '9',
    pygame.K_COLON: 'colon',
    pygame.K_SEMICOLON: 'semicolon',
    pygame.K_LESS: 'less',
    pygame.K_EQUALS: 'equals',
    pygame.K_GREATER: 'greater',
    pygame.K_QUESTION: 'question',
    pygame.K_AT: 'at',
    pygame.K_LEFTBRACKET: 'leftbracket',
    pygame.K_BACKSLASH: 'backslash',
    pygame.K_RIGHTBRACKET: 'rightbracket',
    pygame.K_CARET: 'caret',
    pygame.K_UNDERSCORE: 'underscore',
    pygame.K_BACKQUOTE: 'backquote',
    pygame.K_a: 'a',
    pygame.K_b: 'b',
    pygame.K_c: 'c',
    pygame.K_d: 'd',
    pygame.K_e: 'e',
    pygame.K_f: 'f',
    pygame.K_g: 'g',
    pygame.K_h: 'h',
    pygame.K_i: 'i',
    pygame.K_j: 'j',
    pygame.K_k: 'k',
    pygame.K_l: 'l',
    pygame.K_m: 'm',
    pygame.K_n: 'n',
    pygame.K_o: 'o',
    pygame.K_p: 'p',
    pygame.K_q: 'q',
    pygame.K_r: 'r',
    pygame.K_s: 's',
    pygame.K_t: 't',
    pygame.K_u: 'u',
    pygame.K_v: 'v',
    pygame.K_w: 'w',
    pygame.K_x: 'x',
    pygame.K_y: 'y',
    pygame.K_z: 'z',
    pygame.K_DELETE: 'delete',
    pygame.K_KP0: 'kp0',
    pygame.K_KP1: 'kp1',
    pygame.K_KP2: 'kp2',
    pygame.K_KP3: 'kp3',
    pygame.K_KP4: 'kp4',
    pygame.K_KP5: 'kp5',
    pygame.K_KP6: 'kp6',
    pygame.K_KP7: 'kp7',
    pygame.K_KP8: 'kp8',
    pygame.K_KP9: 'kp9',
    pygame.K_KP_PERIOD: 'kp_period',
    pygame.K_KP_DIVIDE: 'kp_divide',
    pygame.K_KP_MULTIPLY: 'kp_multiply',
    pygame.K_KP_MINUS: 'kp_minus',
    pygame.K_KP_PLUS: 'kp_plus',
    pygame.K_KP_ENTER: 'kp_enter',
    pygame.K_KP_EQUALS: 'kp_equals',
    pygame.K_UP: 'up',
    pygame.K_DOWN: 'down',
    pygame.K_RIGHT: 'right',
    pygame.K_LEFT: 'left',
    pygame.K_INSERT: 'insert',
    pygame.K_HOME: 'home',
    pygame.K_END: 'end',
    pygame.K_PAGEUP: 'pageup',
    pygame.K_PAGEDOWN: 'pagedown',
    pygame.K_F1: 'f1',
    pygame.K_F2: 'f2',
    pygame.K_F3: 'f3',
    pygame.K_F4: 'f4',
    pygame.K_F5: 'f5',
    pygame.K_F6: 'f6',
    pygame.K_F7: 'f7',
    pygame.K_F8: 'f8',
    pygame.K_F9: 'f9',
    pygame.K_F10: 'f10',
    pygame.K_F11: 'f11',
    pygame.K_F12: 'f12',
    pygame.K_F13: 'f13',
    pygame.K_F14: 'f14',
    pygame.K_F15: 'f15',
    pygame.K_NUMLOCK: 'numlock',
    pygame.K_CAPSLOCK: 'capslock',
    pygame.K_SCROLLOCK: 'scrollock',
    pygame.K_RSHIFT: 'rshift',
    pygame.K_LSHIFT: 'lshift',
    pygame.K_RCTRL: 'rctrl',
    pygame.K_LCTRL: 'lctrl',
    pygame.K_RALT: 'ralt',
    pygame.K_LALT: 'lalt',
    pygame.K_RMETA: 'rmeta',
    pygame.K_LMETA: 'lmeta',
    pygame.K_LSUPER: 'lsuper',
    pygame.K_RSUPER: 'rsuper',
    pygame.K_MODE: 'mode',
    pygame.K_HELP: 'help',
    pygame.K_PRINT: 'print',
    pygame.K_SYSREQ: 'sysreq',
    pygame.K_BREAK: 'break',
    pygame.K_MENU: 'menu',
    pygame.K_POWER: 'power',
    pygame.K_EURO: 'euro',
}
