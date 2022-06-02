const fs = require("fs");

const InputData = {};

function createCampSectionData() {
  let CampSectionData = {};

  for (let i = 1; i <= 6; i++) {
    let section = "A" + i;
    CampSectionData[section] = { size: 26110, width: 70 };
  }

  for (let i = 1; i <= 32; i++) {
    let section = "B" + i;
    CampSectionData[section] = { size: 20440, width: 70 };
  }

  for (let i = 1; i <= 32; i++) {
    let section = "C" + i;
    CampSectionData[section] = { size: 14700, width: 70 };
  }

  for (let i = 1; i <= 10; i++) {
    let section = "D" + i;
    CampSectionData[section] = { size: 10500, width: 70 };
  }
  InputData.CampSectionData = CampSectionData;
}

async function editInputData() {
  const areaPerPerson = 140.08;
  fs.readFile("InputData.json", (err, data) => {
    if (err) throw err;
    let campData = JSON.parse(data);
    const { camps } = campData;
    const names = Object.keys(camps);

    names.forEach((name) => {
      camps[name] = Math.floor(camps[name] * areaPerPerson);
    });
    console.log(camps);
    InputData.camps = camps;
  });
}

async function writeToJson() {
  let data = JSON.stringify(InputData, null, 2);
  fs.writeFileSync("InputData.json", data);
}

(async () => {
  await createCampSectionData();
  await editInputData();
  await writeToJson();
})();
