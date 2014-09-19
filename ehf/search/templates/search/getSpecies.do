/**
 * Created by jacky on 14-3-14.
 */

// this script get the corresponding species based on the kingdom, and change the species select

var text = "<select id='pathogen_species_{{row}}' name ='pathogen_species_{{row}}' multiple class='form-control'>\
               <option selected>all</option>\
               {% for speciesItem in species %}\
                    <option>{{ speciesItem }}</option>\
               {% endfor %}\
           </select>\
";

// change the html
var aDiv = document.getElementById("pathogenParmDiv_species_" + {{ row }});
aDiv.innerHTML = text;

