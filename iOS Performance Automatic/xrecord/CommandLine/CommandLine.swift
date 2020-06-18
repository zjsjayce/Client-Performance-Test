/*
 * CommandLine.swift
 * Copyright (c) 2014 Ben Gollmer.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/* Required for setlocale(3) */
import Darwin

let ShortOptionPrefix = "-"
let LongOptionPrefix = "--"

/* Stop parsing arguments when an ArgumentStopper (--) is detected. This is a GNU getopt
 * convention; cf. https://www.gnu.org/prep/standards/html_node/Command_002dLine-Interfaces.html
 */
let ArgumentStopper = "--"

/* Allow arguments to be attached to flags when separated by this character.
 * --flag=argument is equivalent to --flag argument
 */
let ArgumentAttacher: Character = "="

/**
 * The CommandLine class implements a command-line interface for your app.
 * 
 * To use it, define one or more Options (see Option.swift) and add them to your
 * CommandLine object, then invoke parse(). Each Option object will be populated with
 * the value given by the user.
 *
 * If any required options are missing or if an invalid value is found, parse() will return
 * false. You can then call printUsage() to output an automatically-generated usage message.
 */
open class CommandLine {
  fileprivate var _arguments: [String]
  fileprivate var _options: [Option] = [Option]()
  
  /**
   * Initializes a CommandLine object.
   *
   * - parameter arguments: Arguments to parse. If omitted, the arguments passed to the app
   *   on the command line will automatically be used.
   *
   * - returns: An initalized CommandLine object.
   */
  public init(arguments: [String] = Swift.CommandLine.arguments) {
    self._arguments = arguments
    
    /* Initialize locale settings from the environment */
    setlocale(LC_ALL, "")
  }
  
  /* Returns all argument values from flagIndex to the next flag or the end of the argument array. */
  fileprivate func _getFlagValues(flagIndex: Int) -> [String] {
    var args: [String] = [String]()
    var skipFlagChecks = false
    
    /* Grab attached arg, if any */
    var attachedArg = _arguments[flagIndex].splitByCharacter(ArgumentAttacher, maxSplits: 1)
    if attachedArg.count > 1 {
      args.append(attachedArg[1])
    }
    
    for i in flagIndex + 1 ..< _arguments.count {
      if !skipFlagChecks {
        if _arguments[i] == ArgumentStopper {
          skipFlagChecks = true
          continue
        }
        
        if _arguments[i].hasPrefix(ShortOptionPrefix) && Int(_arguments[i]) == nil &&
          _arguments[i].toDouble() == nil {
          break
        }
      }
    
      args.append(_arguments[i])
    }
    
    return args
  }
  
  /**
   * Adds an Option to the command line.
   *
   * - parameter option: The option to add.
   */
  open func addOption(_ option: Option) {
    _options.append(option)
  }
  
  /**
   * Adds one or more Options to the command line.
   *
   * - parameter options: An array containing the options to add.
   */
  open func addOptions(_ options: [Option]) {
    _options += options
  }
  
  /**
   * Adds one or more Options to the command line.
   *
   * - parameter options: The options to add.
   */
  open func addOptions(_ options: Option...) {
    _options += options
  }
  
  /**
   * Sets the command line Options. Any existing options will be overwritten.
   *
   * - parameter options: An array containing the options to set.
   */
  open func setOptions(_ options: [Option]) {
    _options = options
  }
  
  /**
   * Sets the command line Options. Any existing options will be overwritten.
   *
   * - parameter options: The options to set.
   */
  open func setOptions(_ options: Option...) {
    _options = options
  }
  
  /**
   * Parses command-line arguments into their matching Option values.
   *
   * - returns: True if all arguments were parsed successfully, false if any option had an
   *   invalid value or if a required option was missing.
   */
  open func parse() -> (Bool, String?) {
    
    for (idx, arg) in _arguments.enumerated() {
      if arg == ArgumentStopper {
        break
      }
      
      if !arg.hasPrefix(ShortOptionPrefix) {
        continue
      }
      
      /* Swift strings don't have substringFromIndex(). Do a little dance instead. */
      var flag = ""
      var skipChars =
        arg.hasPrefix(LongOptionPrefix) ? LongOptionPrefix.characters.count : ShortOptionPrefix.characters.count
      for c in arg.characters {
        if skipChars > 0 {
          skipChars -= 1
          continue
        }
        
        flag.append(c)
      }
      
      /* Remove attached argument from flag */
      flag = flag.splitByCharacter(ArgumentAttacher, maxSplits: 1)[0]
      
      var flagMatched = false
      for option in _options {
        if flag == option.shortFlag || flag == option.longFlag {
          let vals = self._getFlagValues(flagIndex: idx)
          if !option.match(vals) {
            return (false, "Invalid value for \(option.longFlag)")
          }
          
          flagMatched = true
          break
        }
      }
      
      /* Flags that do not take any arguments can be concatenated */
      if !flagMatched && !arg.hasPrefix(LongOptionPrefix) {
        for (i, c) in flag.characters.enumerated() {
          let flagLength = flag.characters.count
          for option in _options {
            if String(c) == option.shortFlag {
              /* Values are allowed at the end of the concatenated flags, e.g.
               * -xvf <file1> <file2>
               */
              let vals = (i == flagLength - 1) ? self._getFlagValues(flagIndex: idx) : [String]()
              if !option.match(vals) {
                return (false, "Invalid value for \(option.longFlag)")
              }
              
              break
            }
          }
        }
      }
    }

    /* Check to see if any required options were not matched */
    for option in _options {
      if option.required && !option.isSet {
        return (false, "\(option.longFlag) is required")
      }
    }
    
    return (true, nil)
  }
  
  /** Prints a usage message to stdout. */
  open func printUsage() {
    let name = _arguments[0]
    
    var flagWidth = 0
    for opt in _options {
      flagWidth = max(flagWidth,
        "  \(ShortOptionPrefix)\(opt.shortFlag), \(LongOptionPrefix)\(opt.longFlag):".characters.count)
    }
    
    print("Usage: \(name) [options]")
    for opt in _options {
      let flags = "  \(ShortOptionPrefix)\(opt.shortFlag), \(LongOptionPrefix)\(opt.longFlag):".paddedToWidth(flagWidth)
      
      print("\(flags)\n      \(opt.helpMessage)")
    }
  }
}
