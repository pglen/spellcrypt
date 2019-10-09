// Copyright 2000 by Kevin Atkinson under the terms of the LGPL

#ifndef ASPELLER_DATA__HPP
#define ASPELLER_DATA__HPP

#include <assert.h>

#include "copy_ptr.hpp"
#include "enumeration.hpp"
#include "language.hpp"
#include "posib_err.hpp"
#include "string.hpp"
#include "string_enumeration.hpp"
#include "word_list.hpp"
#include "cache.hpp"
#include "wordinfo.hpp"

using namespace acommon;

namespace acommon {
  class Config;
  class FStream;
  class OStream;
  class Convert;
}

namespace aspeller {

  class Dictionary;
  struct SensitiveCompare {};

  struct LocalDict 
  {
    Dictionary * dict;
    const SensitiveCompare * compare;
  };

  typedef Enumeration<WordEntry *> WordEntryEnumeration;
  typedef Enumeration<const LocalDict *> DictsEnumeration;

  class Dictionary : public Cacheable, public WordList {

    virtual ~Dictionary();

    const Language * language() const = 0;
    const char * lang_name() const = 0;

    const char * file_name() const {return file_name_.path.c_str();}
    // returns any additional dictionaries that are also used
    virtual PosibErr<void> load(ParmString, const Config &) = 0;

    // FIXME: do I need all these?????
    virtual PosibErr<void> merge(ParmString) = 0;
    virtual PosibErr<void> synchronize() = 0;
    virtual PosibErr<void> save_noupdate() = 0;
    virtual PosibErr<void> save_as(ParmString) = 0;
    virtual PosibErr<void> clear() = 0;

    StringEnumeration * elements() const;

    virtual WordEntryEnumeration * detailed_elements() const = 0;
    virtual size_t size()     const;
    virtual bool   empty()    const;
  
    virtual bool lookup(ParmString word, WordEntry &, 
                        const SensitiveCompare &) const = 0;
    
    virtual bool stripped_lookup(ParmString, WordEntry &) const = 0;

    virtual bool soundslike_lookup(ParmString, WordEntry & o) const = 0;

    virtual PosibErr<void> add(ParmString w) = 0;

    virtual PosibErr<void> remove(ParmString w) = 0;

    virtual bool repl_lookup(ParmString, WordEntry &) const = 0;

    PosibErr<void> add_repl(ParmString mis, ParmString cor) = 0;

    virtual PosibErr<void> remove_repl(ParmString mis, ParmString cor) = 0;

    virtual DictsEnumeration * dictionaries() const = 0;
  };

  bool operator==(const Dictionary::Id & rhs, const Dictionary::Id & lhs);

  inline bool operator!=(const  Dictionary::Id & rhs, const Dictionary::Id & lhs)
  {
    return !(rhs == lhs);
  }

  // stores result in LocalDict
  // any new extra dictionaries that were loaded will be ii
  PosibErr<LocalDict *> new_dict(ParmString file_name, const Config &);

  // implemented in readonly_ws.cc
  Dictionary * new_default_readonly_dict();
  
  PosibErr<void> create_default_readonly_dict(StringEnumeration * els,
                                              Config & config);
  
  // implemented in multi_ws.cc
  MultiDict * new_default_multi_dict();

  // implemented in writable.cpp
  Dictionary * new_default_writable_dict();

  // implemented in writable.cpp
  ReplacementDict * new_default_replacement_dict();
}

#endif

