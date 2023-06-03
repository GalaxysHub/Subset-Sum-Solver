const fs = require("fs");
const InputData = require("./InputData.json");

const CampAreasMap = InputData.OmittedCamps;

let formatedSolution = {};

async function run() {
  let rawData = await fs.readFileSync("solution.json");
  let solution = JSON.parse(rawData);
  // await specialCases(solution);
  await formatSolution(solution);
  await writeSolution();
}

var reA = /[^a-zA-Z]/g;
var reN = /[^0-9]/g;

function sortAlphaNum(a, b) {
  var aA = a.replace(reA, "");
  var bA = b.replace(reA, "");
  if (aA === bA) {
    var aN = parseInt(a.replace(reN, ""), 10);
    var bN = parseInt(b.replace(reN, ""), 10);
    return aN === bN ? 0 : aN > bN ? 1 : -1;
  } else {
    return aA > bA ? 1 : -1;
  }
}

async function specialCases(solution) {
  const { Sections, CampAreas, Camps, CampLengths } = solution;

  Sections.forEach(async (section, i) => {
    if (section === "C32") {
      //add Camp Schwifty 2020!
      Camps[i].push("Camp Schwifty 2020!");
      CampAreas[i].push(CampAreasMap["Camp Schwifty 2020!"]);
      CampLengths[i].push(Math.round(CampAreasMap["Camp Schwifty 2020!"] / 70));
      //Add M3ga St3llar Ali3ns
      Camps[i].push("M3ga St3llar Ali3ns");
      CampAreas[i].push(CampAreasMap["M3ga St3llar Ali3ns"]);
      CampLengths[i].push(Math.round(CampAreasMap["M3ga St3llar Ali3ns"] / 70));
    } else if (section === "B32") {
      // add slippery saucy sloots
      Camps[i].push("slippery saucy sloots");
      CampAreas[i].push(CampAreasMap["slippery saucy sloots"]);
      CampLengths[i].push(
        Math.round(CampAreasMap["slippery saucy sloots"] / 70)
      );
      //Add cabbage pash kids`
      Camps[i].push("cabbage pash kids");
      CampAreas[i].push(CampAreasMap["cabbage pash kids"]);
      CampLengths[i].push(Math.round(CampAreasMap["cabbage pash kids"] / 70));
    }
    const CampNames = Camps[i];
    CampNames.forEach((campName, j) => {
      if (campName === "Camp Ohana x2") {
        //separate 2 camp ohanas
        Camps[i].splice(j, 1, "Ohana 1", "Ohana 2");
        CampAreas[i].splice(
          j,
          1,
          CampAreasMap["Camp Ohana 1"],
          CampAreasMap["Camp Ohana 2"]
        );
        CampLengths[i].splice(
          j,
          1,
          Math.round(CampAreasMap["Camp Ohana 1"] / 70),
          Math.round(CampAreasMap["Camp Ohana 2"] / 70)
        );
      } else if (campName === "TEAM BLAST OFF & Camp Wurder") {
        //seprate Team Blast Off and Camp Wurder
        Camps[i].splice(j, 1, "TEAM BLAST OFF", "Camp Wurder");
        CampAreas[i].splice(
          j,
          1,
          CampAreasMap["TEAM BLAST OFF"],
          CampAreasMap["Camp Wurder"]
        );
        CampLengths[i].splice(
          j,
          1,
          Math.round(CampAreasMap["TEAM BLAST OFF"] / 70),
          Math.round(CampAreasMap["Camp Wurder"] / 70)
        );
      }
    });
  });
}

async function formatSolution(solution) {
  const { Sections, CampAreas, Camps, CampLengths } = solution;

  //Sort setions alphanumerically
  const SectionsMap = {};

  Sections.forEach((section, i) => {
    SectionsMap[section] = {
      groupCamps: Camps[i],
      camp_lengths: CampLengths[i],
      camp_areas: CampAreas[i],
    };
  });

  const sortedSections = Object.keys(SectionsMap).sort(sortAlphaNum);
  console.log("sortedSections =>", sortedSections);

  sortedSections.forEach((section, i) => {
    const { groupCamps, camp_lengths, camp_areas } = SectionsMap[section];
    groupCamps.forEach((camp, j) => {
      let sectionIndex = section + "-" + String.fromCharCode(65 + j);
      let campLength = camp_lengths[j];
      let campArea = camp_areas[j];
      let width = Math.round(campArea / campLength);
      formatedSolution[sectionIndex] = {
        name: camp,
        length: campLength,
        width,
      };
    });
  });
}

async function writeSolution() {
  await fs.writeFileSync(
    "formatedSolution.json",
    JSON.stringify(formatedSolution, null, 4)
  );

  let data = "Camp Section \t Camp \t Length (ft) \t Width (ft) \n";
  for (const [CampIndex, CampData] of Object.entries(formatedSolution)) {
    data =
      data +
      CampIndex +
      "\t" +
      CampData.name +
      "\t" +
      CampData.length +
      "\t" +
      CampData.width +
      "\n";
  }

  await fs.appendFile("formatedSolution.csv", data, (err) => {
    if (err) throw err;
  });
}

(async () => {
  try {
    await run();
    console.log("format successful");
  } catch (err) {
    console.log("err =>", err);
  }
})();
