#!/usr/bin/env python3
"""
Generate a Hazel .hazelrules file for deleting folders without audio files.

Creates two rules:
  1. "Recurse into subfolders" - Kind is Folder → Run rules on folder contents
  2. "Delete folders without audio" - Kind is Folder + Passes shell script → Move to Trash

The file is constructed in NSKeyedArchiver plist format, matching the serialization
structure used by Hazel (Noodlesoft).
"""

import plistlib
import os
import sys

SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "no_audio_in_folder.sh")

def uid(n):
    """Create a CF$UID reference."""
    return {"CF$UID": n}

def build_hazelrules():
    objects = []
    # Index 0: $null sentinel
    objects.append("$null")  # 0

    # ========================================================================
    # Class definition objects (reused across rules)
    # We'll place these at known indices and reference them by index.
    # ========================================================================

    # --- Index 1: NSSelfExpression class def ---
    objects.append({
        "$classes": ["NSSelfExpression", "NSExpression", "NSObject"],
        "$classname": "NSSelfExpression",
    })  # 1

    # --- Index 2: NSSelfExpression instance ---
    objects.append({
        "$class": uid(1),
        "NSExpressionType": 1,
    })  # 2

    # --- Index 3: NSKeyPathSpecifierExpression class def ---
    objects.append({
        "$classes": ["NSKeyPathSpecifierExpression", "NSExpression", "NSObject"],
        "$classname": "NSKeyPathSpecifierExpression",
    })  # 3

    # --- Index 4: NSMutableArray class def ---
    objects.append({
        "$classes": ["NSMutableArray", "NSArray", "NSObject"],
        "$classname": "NSMutableArray",
    })  # 4

    # --- Index 5: NSKeyPathExpression class def ---
    objects.append({
        "$classes": ["NSKeyPathExpression", "NSFunctionExpression", "NSExpression", "NSObject"],
        "$classname": "NSKeyPathExpression",
    })  # 5

    # --- Index 6: NSConstantValueExpression class def ---
    objects.append({
        "$classes": ["NSConstantValueExpression", "NSExpression", "NSObject"],
        "$classname": "NSConstantValueExpression",
    })  # 6

    # --- Index 7: NSEqualityPredicateOperator class def ---
    objects.append({
        "$classes": ["NSEqualityPredicateOperator", "NSPredicateOperator", "NSObject"],
        "$classname": "NSEqualityPredicateOperator",
    })  # 7

    # --- Index 8: NSComparisonPredicate class def ---
    objects.append({
        "$classes": ["NSComparisonPredicate", "NSPredicate", "NSObject"],
        "$classname": "NSComparisonPredicate",
    })  # 8

    # --- Index 9: NSCustomPredicateOperator class def ---
    objects.append({
        "$classes": ["NSCustomPredicateOperator", "NSPredicateOperator", "NSObject"],
        "$classname": "NSCustomPredicateOperator",
    })  # 9

    # --- Index 10: ComNoodlesoft_HazelRule class def ---
    objects.append({
        "$classes": ["ComNoodlesoft_HazelRule", "NSObject"],
        "$classname": "ComNoodlesoft_HazelRule",
    })  # 10

    # --- Index 11: ComNoodlesoft_HazelMoveAction class def ---
    objects.append({
        "$classes": ["ComNoodlesoft_HazelMoveAction", "ComNoodlesoft_HazelAction", "NSObject"],
        "$classname": "ComNoodlesoft_HazelMoveAction",
    })  # 11

    # --- Index 12: ComNoodlesoft_HazelTrashFolder class def ---
    objects.append({
        "$classes": ["ComNoodlesoft_HazelTrashFolder", "ComNoodlesoft_HazelFolder", "NSObject"],
        "$classname": "ComNoodlesoft_HazelTrashFolder",
    })  # 12

    # --- Index 13: ComNoodlesoft_HazelRuleSet class def ---
    objects.append({
        "$classes": ["ComNoodlesoft_HazelRuleSet", "NSObject"],
        "$classname": "ComNoodlesoft_HazelRuleSet",
    })  # 13

    # --- Index 14: NSMutableDictionary class def ---
    objects.append({
        "$classes": ["NSMutableDictionary", "NSDictionary", "NSObject"],
        "$classname": "NSMutableDictionary",
    })  # 14

    # --- Index 15: ComNoodlesoft_HazelSubfolderAction class def ---
    objects.append({
        "$classes": ["ComNoodlesoft_HazelSubfolderAction", "ComNoodlesoft_HazelAction", "NSObject"],
        "$classname": "ComNoodlesoft_HazelSubfolderAction",
    })  # 15

    # --- Index 16: NSCompoundPredicate class def ---
    objects.append({
        "$classes": ["NSCompoundPredicate", "NSPredicate", "NSObject"],
        "$classname": "NSCompoundPredicate",
    })  # 16

    # --- Index 17: NSArray class def ---
    objects.append({
        "$classes": ["NSArray", "NSObject"],
        "$classname": "NSArray",
    })  # 17

    # --- Index 18: string "valueForKey:" ---
    objects.append("valueForKey:")  # 18

    # --- Index 19: string "kind" (keypath for Kind attribute) ---
    objects.append("kind")  # 19

    # --- Index 20: string "public.folder" (UTI for folders) ---
    objects.append("public.folder")  # 20

    # --- Index 21: predicateTarget value 0 (match on file/folder itself) ---
    objects.append(0)  # 21

    # ========================================================================
    # Build the "Kind is Folder" NSComparisonPredicate
    # Pattern: SELF.kind == "public.folder"
    # ========================================================================

    # --- Index 22: NSKeyPathSpecifierExpression for "kind" ---
    objects.append({
        "$class": uid(3),
        "NSExpressionType": 10,
        "NSKeyPath": uid(19),
    })  # 22

    # --- Index 23: NSMutableArray wrapping the keypath expr (arguments) ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(22)],
    })  # 23

    # --- Index 24: NSKeyPathExpression (valueForKey: on SELF with "kind") ---
    objects.append({
        "$class": uid(5),
        "NSArguments": uid(23),
        "NSExpressionType": 3,
        "NSOperand": uid(2),
        "NSSelectorName": uid(18),
    })  # 24

    # --- Index 25: NSConstantValueExpression for "public.folder" ---
    objects.append({
        "$class": uid(6),
        "NSConstantValue": uid(20),
        "NSExpressionType": 0,
    })  # 25

    # --- Index 26: NSEqualityPredicateOperator (equals, case+diacritic insensitive) ---
    objects.append({
        "$class": uid(7),
        "NSModifier": 0,
        "NSNegate": False,
        "NSOperatorType": 4,
        "NSOptions": 3,
    })  # 26

    # --- Index 27: NSComparisonPredicate (kind == public.folder) ---
    # This is the "Kind is Folder" condition
    objects.append({
        "$class": uid(8),
        "NSLeftExpression": uid(24),
        "NSPredicateOperator": uid(26),
        "NSRightExpression": uid(25),
    })  # 27

    # ========================================================================
    # Build the "Passes shell script" condition
    # This uses a custom predicate: SELF.shellScript(<path>) matches
    # ========================================================================

    # --- Index 28: string "passesShellScript" ---
    objects.append("passesShellScript")  # 28

    # --- Index 29: the shell script path ---
    objects.append(SCRIPT_PATH)  # 29

    # --- Index 30: NSKeyPathSpecifierExpression for "passesShellScript" ---
    objects.append({
        "$class": uid(3),
        "NSExpressionType": 10,
        "NSKeyPath": uid(28),
    })  # 30

    # --- Index 31: NSMutableArray wrapping the keypath expr ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(30)],
    })  # 31

    # --- Index 32: NSKeyPathExpression (valueForKey: on SELF with passesShellScript) ---
    objects.append({
        "$class": uid(5),
        "NSArguments": uid(31),
        "NSExpressionType": 3,
        "NSOperand": uid(2),
        "NSSelectorName": uid(18),
    })  # 32

    # --- Index 33: NSConstantValueExpression for the script path ---
    objects.append({
        "$class": uid(6),
        "NSConstantValue": uid(29),
        "NSExpressionType": 0,
    })  # 33

    # --- Index 34: string "hazelPassesScript:" ---
    objects.append("hazelPassesScript:")  # 34

    # --- Index 35: NSCustomPredicateOperator for shell script ---
    objects.append({
        "$class": uid(9),
        "NSModifier": 0,
        "NSOperatorType": 11,
        "NSSelectorName": uid(34),
    })  # 35

    # --- Index 36: NSComparisonPredicate for shell script ---
    objects.append({
        "$class": uid(8),
        "NSLeftExpression": uid(32),
        "NSPredicateOperator": uid(35),
        "NSRightExpression": uid(33),
    })  # 36

    # ========================================================================
    # Rule 1: "Recurse into subfolders"
    #   Condition: Kind is Folder (single condition)
    #   Action: Run rules on folder contents
    # ========================================================================

    # --- Index 37: criteria array for Rule 1 (just "Kind is Folder") ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(27)],
    })  # 37

    # --- Index 38: ComNoodlesoft_HazelSubfolderAction ---
    objects.append({
        "$class": uid(15),
        "options": uid(39),
        "parameter": uid(0),
    })  # 38

    # --- Index 39: empty options dict for subfolder action ---
    objects.append({
        "$class": uid(14),
        "NS.keys": [],
        "NS.objects": [],
    })  # 39

    # --- Index 40: actions array for Rule 1 ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(38)],
    })  # 40

    # --- Index 41: string "Recurse into subfolders" ---
    objects.append("Recurse into subfolders")  # 41

    # --- Index 42: Rule 1 (ComNoodlesoft_HazelRule) ---
    objects.append({
        "$class": uid(10),
        "actions": uid(40),
        "criteria": uid(37),
        "dateLastModified": uid(0),
        "description": uid(41),
        "isActive": True,
        "predicateTarget": uid(21),
        "predicateType": 1,
    })  # 42

    # ========================================================================
    # Rule 2: "Delete folders without audio"
    #   Conditions (ALL): Kind is Folder + Passes shell script
    #   Action: Move to Trash
    # ========================================================================

    # We need a second "Kind is Folder" predicate or reuse #27.
    # NSKeyedArchiver allows reuse, so we can reference #27 again.

    # --- Index 43: criteria array for Rule 2 (Kind is Folder + shell script) ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(27), uid(36)],
    })  # 43

    # --- Index 44: ComNoodlesoft_HazelTrashFolder instance ---
    objects.append({
        "$class": uid(12),
        "identifier": uid(45),
        "isPaused": False,
    })  # 44

    # --- Index 45: string "trash" ---
    objects.append("trash")  # 45

    # --- Index 46: options dict for move action (throwAwayDupes, replaceExisting) ---
    objects.append({
        "$class": uid(14),
        "NS.keys": [uid(47), uid(48)],
        "NS.objects": [uid(49), uid(49)],
    })  # 46

    # --- Index 47: string "throwAwayDupes" ---
    objects.append("throwAwayDupes")  # 47

    # --- Index 48: string "replaceExisting" ---
    objects.append("replaceExisting")  # 48

    # --- Index 49: false value ---
    objects.append(False)  # 49

    # --- Index 50: ComNoodlesoft_HazelMoveAction (move to trash) ---
    objects.append({
        "$class": uid(11),
        "options": uid(46),
        "parameter": uid(44),
    })  # 50

    # --- Index 51: actions array for Rule 2 ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(50)],
    })  # 51

    # --- Index 52: string "Delete folders without audio" ---
    objects.append("Delete folders without audio")  # 52

    # --- Index 53: Rule 2 (ComNoodlesoft_HazelRule) ---
    objects.append({
        "$class": uid(10),
        "actions": uid(51),
        "criteria": uid(43),
        "dateLastModified": uid(0),
        "description": uid(52),
        "isActive": True,
        "predicateTarget": uid(21),
        "predicateType": 1,
    })  # 53

    # ========================================================================
    # RuleSet (top-level container)
    # ========================================================================

    # --- Index 54: rules array (Rule 1 first, then Rule 2) ---
    objects.append({
        "$class": uid(4),
        "NS.objects": [uid(42), uid(53)],
    })  # 54

    # --- Index 55: options dict for the ruleset (empty) ---
    objects.append({
        "$class": uid(14),
        "NS.keys": [],
        "NS.objects": [],
    })  # 55

    # --- Index 56: version number ---
    objects.append(15)  # 56

    # --- Index 57: ComNoodlesoft_HazelRuleSet instance ---
    objects.append({
        "$class": uid(13),
        "options": uid(55),
        "rules": uid(54),
        "version": uid(56),
    })  # 57

    # Build the full NSKeyedArchiver structure
    archive = {
        "$archiver": "NSKeyedArchiver",
        "$objects": objects,
        "$top": {
            "root": uid(57),
        },
        "$version": 100000,
    }

    return archive


def main():
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "Delete folders without audio.hazelrules",
    )

    archive = build_hazelrules()

    # Write as binary plist (standard Hazel format)
    with open(output_path, "wb") as f:
        plistlib.dump(archive, f, fmt=plistlib.FMT_BINARY)

    print(f"Generated: {output_path}")
    print(f"Shell script path embedded: {SCRIPT_PATH}")
    print()
    print("To import: Open Hazel preferences → select a folder → File → Import Rules")
    print("Or double-click the .hazelrules file.")


if __name__ == "__main__":
    main()
