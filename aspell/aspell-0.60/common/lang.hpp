// Copyright 2000 by Kevin Atkinson under the terms of the LGPL

#ifndef ASPELLER_LANGUAGE__HPP
#define ASPELLER_LANGUAGE__HPP

#include "affix.hpp"
#include "cache.hpp"
#include "config.hpp"
#include "convert.hpp"
#include "phonetic.hpp"
#include "posib_err.hpp"
#include "stack_ptr.hpp"
#include "string.hpp"
#include "objstack.hpp"

using namespace acommon;

namespace acommon {
  struct CheckInfo;
}

namespace aspeller {

  class Language : public Cacheable {

    PosibErr<void> setup(const String & lang, const Config * config);
    void set_lang_defaults(Config & config);

    const char * name() const {return name_.c_str();}
    const char * charset() const {return charset_.c_str();}
  
    String to_soundslike(ParmString word) const {
      return soundslike_->to_soundslike(word);
    }

    const char * soundslike_name() const {
      return soundslike_->name();
    }

    const char * soundslike_version() const {
      return soundslike_->version();
    }
    
    bool have_soundslike() const {return soundslike_;}

    char * to_lower(char *, const char *);
    char * to_upper(char *, const char *);
    char * to_title(char *, const char *);
    char * to_stripped(char *, const char *);
    
    CasePattern case_pattern(const char *);
    char * fix_case(char *, const char *);

    void munch(ParmString word, CheckList *) const;

    WordAff * expand(ParmString word, ParmString aff, 
                     ObjStack &, int limit = INT_MAX) const;
  };

}


#endif
