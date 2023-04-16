const elements = [
    "H", // Hydrogen
    "He", // Helium
    "Li", // Lithium
    "Be", // Beryllium
    "B", // Boron
    "C", // Carbon
    "N", // Nitrogen
    "O", // Oxygen
    "F", // Fluorine
    "Ne", // Neon
    "Na", // Sodium
    "Mg", // Magnesium
    "Al", // Aluminum
    "Si", // Silicon
    "P", // Phosphorus
    "S", // Sulfur
    "Cl", // Chlorine
    "Ar", // Argon
    "K", // Potassium
    "Ca", // Calcium
    "Sc", // Scandium
    "Ti", // Titanium
    "V", // Vanadium
    "Cr", // Chromium
    "Mn", // Manganese
    "Fe", // Iron
    "Co", // Cobalt
    "Ni", // Nickel
    "Cu", // Copper
    "Zn", // Zinc
  ];

function getElementFromAtm(i) {
    if (typeof elements[i-1] === "undefined") {
        throw new Error("Not a valid element")
    }

    return elements[i-1]
}

function intToRoman(num) {
    const romanNumerals = {
      M: 1000,
      CM: 900,
      D: 500,
      CD: 400,
      C: 100,
      XC: 90,
      L: 50,
      XL: 40,
      X: 10,
      IX: 9,
      V: 5,
      IV: 4,
      I: 1,
    };

    let roman = "";

    for (let key in romanNumerals) {
      while (num >= romanNumerals[key]) {
        roman += key;
        num -= romanNumerals[key];
      }
    }

    return roman;
  }
