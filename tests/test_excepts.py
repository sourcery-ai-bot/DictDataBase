import dictdatabase as DDB
from dictdatabase import utils
from path_dict import pd
import pytest


def test_except_during_open_session(env, use_compression, use_orjson, sort_keys, indent):
	name = "test_except_during_open_session"
	d = {"test": "value"}
	DDB.at(name).create(d, force_overwrite=True)
	with pytest.raises(RuntimeError):
		with DDB.at(name).session() as (session, test):
			raise RuntimeError("Any Exception")



def test_except_on_save_unserializable(env, use_compression, use_orjson, sort_keys, indent):
	name = "test_except_on_save_unserializable"
	with pytest.raises(TypeError):
		d = {"test": "value"}
		DDB.at(name).create(d, force_overwrite=True)
		with DDB.at(name).session(as_type=pd) as (session, test):
			test["test"] = {"key": {1, 2}}
			session.write()


def test_except_on_save_unserializable_in_multisession(env, use_compression, use_orjson, sort_keys, indent):
	name = "test_except_on_save_unserializable_in_multisession"
	with pytest.raises(TypeError):
		d = {"test": "value"}
		DDB.at(name, "1").create(d, force_overwrite=True)
		DDB.at(name, "2").create(d, force_overwrite=True)
		with DDB.at(name, "*").session(as_type=pd) as (session, test):
			test["1"]["test"] = {"key": {1, 2}}
			session.write()


def test_except_on_session_in_session(env, use_compression, use_orjson, sort_keys, indent):
	name = "test_except_on_session_in_session"
	d = {"test": "value"}
	DDB.at(name).create(d, force_overwrite=True)
	with pytest.raises(RuntimeError):
		with DDB.at(name).session(as_type=pd) as (session, test):
			with DDB.at(name).session(as_type=pd) as (session2, test2):
				pass


def test_except_on_write_outside_session(env, use_compression, use_orjson, sort_keys, indent):
	with pytest.raises(PermissionError):
		s = DDB.at("test_except_on_write_outside_session").session()
		s.write()


def test_wildcard_and_subkey_except(env, use_compression, use_orjson, sort_keys, indent):
	with pytest.raises(ValueError):
		DDB.at("test_wildcard_and_subkey_except/*").read(key="key")



def test_utils_invalid_json_except(env):
	with pytest.raises(TypeError):
		utils.seek_index_through_value("{This is not { JSON", 0)
