const fs = require("fs");
const InputData = require("./InputData.json");

const CampAreasMap = InputData.OmittedCamps;

let formatedSolution = {};

async function run() {
  let rawData = await fs.readFileSync("solution.json");
  let solution = JSON.parse(rawData);
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

  await fs.writeFile("formatedSolution.csv", data, (err) => {
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
