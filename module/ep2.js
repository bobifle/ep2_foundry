// Import Modules
import { Ep2Actor } from "./actor/actor.js";
import { Ep2ActorSheet } from "./actor/actor-sheet.js";
import { Ep2Item } from "./item/item.js";
import { Ep2ItemSheet } from "./item/item-sheet.js";

Hooks.once('init', async function() {

  game.ep2 = {
    Ep2Actor,
    Ep2Item
  };

  /**
   * Set an initiative formula for the system
   * @type {String}
   */
  CONFIG.Combat.initiative = {
    formula: "1d20",
    decimals: 2
  };

  // Define custom Entity classes
  CONFIG.Actor.entityClass = Ep2Actor;
  CONFIG.Item.entityClass = Ep2Item;

  // Register sheet application classes
  Actors.unregisterSheet("core", ActorSheet);
  Actors.registerSheet("ep2", Ep2ActorSheet, { makeDefault: true });
  Items.unregisterSheet("core", ItemSheet);
  Items.registerSheet("ep2", Ep2ItemSheet, { makeDefault: true });

  // If you need to add Handlebars helpers, here are a few useful examples:
  Handlebars.registerHelper('concat', function() {
    var outStr = '';
    for (var arg in arguments) {
      if (typeof arguments[arg] != 'object') {
        outStr += arguments[arg];
      }
    }
    return outStr;
  });

  Handlebars.registerHelper('toLowerCase', function(str) {
    return str.toLowerCase();
  });
});
