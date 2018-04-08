#!/usr/bin/env python3


from enum import Enum, auto
from time import monotonic


class PointerAxis(Enum):
	"""An enumeration describing pointer scrolling axis.
	"""

	VERTICAL = auto()
	HORIZONTAL = auto()


class WindowEventType(Enum):
	"""An enumeration describing whether window was created, destroyed
	or focused.
	"""

	CREATED = auto()
	DESTROYED = auto()
	FOCUSED = auto()


class WindowState(Enum):
	"""An enumeration describing window state.
	"""

	NORMAL = auto()
	MINIMIZED = auto()
	MAXIMIZED = auto()


class Event(object):
	"""Base class for all macpy events.

	Attributes:
		time (:class:`float`): Event timestamp. This does not translate to
			concrete time but timestamps of later events are guaranteed to be
			greater than timestamps of earlier events.
	"""

	def __init__(self):

		self.time = monotonic()

	def __repr__(self):

		items = []
		for name, attr in self.__dict__.items():
			if not name.startswith('_'):
				items.append('{0}={1}'.format(name, repr(attr)))
		items.sort()
		return '<{0}: {1}>'.format(self.__class__.__name__, ', '.join(items))


class PointerEventMotion(Event):
	"""Event representing pointer movement on screen.

	Attributes:
		position (:class:`tuple`): A namedtuple containing x and y coordinates
			of pointer on screen.
		modifiers (:class:`tuple`): A namedtuple containing modifier state at
			the time of this event.
	"""

	def __init__(self, position, modifiers):

		super().__init__()
		self.position = position
		self.modifiers = modifiers


class PointerEventButton(Event):
	"""Event representing button events on connected pointing devices.

	Attributes:
		button (:class:`~macpy.key.Key`): Button that was pressed/released.
		state (:class:`~macpy.key.KeyState`): Whether button was pressed or
			released.
		modifiers (:class:`tuple`): A namedtuple containing modifier state at
			the time of this event.
	"""

	def __init__(self, button, state, modifiers):

		super().__init__()
		self.button = button
		self.state = state
		self.modifiers = modifiers


class PointerEventAxis(Event):
	"""Event representing scrolling.

	Attributes:
		value (:class:`float`): The amount scrolled. This is platform dependent.
		axis (:class:`.PointerAxis`): The axis along which scrolling ocured.
		modifiers (:class:`tuple`): A namedtuple containing modifier state at
			the time of this event.
	"""

	def __init__(self, value, axis, modifiers):

		super().__init__()
		self.value = value
		self.axis = axis
		self.modifiers = modifiers


class KeyboardEvent(Event):
	"""Event representing key press/release on connected keyboards.

	Attributes:
		key (:class:`~macpy.key.Key`): The key that was pressed/released.
		state (:class:`~macpy.key.KeyState`): Whether the key was pressed or
			released.
		char (:class:`str`): The character produced by this key event if any.
		modifiers (:class:`tuple`): A namedtuple containing modifier state at
			the time of this event.
		locks (:class:`tuple`): A namedtuple containing lock key state at the
			time of this event.
	"""

	def __init__(self, key, state, char, modifiers, locks):

		super().__init__()
		self.key = key
		self.state = state
		self.char = char
		self.modifiers = modifiers
		self.locks = locks


class HotKey(Event):
	"""A hotkey object.

	Hotkey object are hashable and compare equal regardless of timestamps.

	Attributes:
		key (:class:`~macpy.key.Key`): A key that triggered this event.
		modifiers (:class:`frozenset`): A frozenset of modifier keys that were
			also pressed.
	"""

	def __init__(self, key, modifiers):

		super().__init__()
		self.key = key
		self.modifiers = frozenset(modifiers)

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return self.key == other.key and self.modifiers == other.modifiers
		else:
			return NotImplemented

	def __hash__(self):

		return hash((self.key, self.modifiers))


class HotString(Event):
	"""A hotstring object.

	Hotstring objects are hashable and compare equal regardless of timestamps
	and the current trigger.

	Attributes:
		string (:class:`str`): The string that needs to be typed to trigger
			this hotstring.
		triggers (:class:`frozenset`): The trigger keys that need to be typed
			after the string. This frozenset may be empty.
		trigger (:class:`str`): The trigger that triggered this hotstring.
			May be :obj:`None`.
	"""

	def __init__(self, string, triggers, trigger=None):

		super().__init__()
		self.string = string
		self.triggers = frozenset(triggers)
		self.trigger = trigger

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return (
				self.string == other.string and self.triggers == other.triggers)
		else:
			return NotImplemented

	def __hash__(self):

		return hash((self.string, self.triggers))


class WindowEvent(Event):
	"""Event representing window creation, destruction and focus change.

	Attributes:
		window (:class:`~macpy.Window`): The window that was
			created/destroyed/focused.
		type (:class:`.WindowEventType`): The action that was taken on
			the window.
	"""

	def __init__(self, window, event_type):

		super().__init__()
		self.window = window
		self.type = event_type