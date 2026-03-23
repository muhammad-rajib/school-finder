export type LocationTree = Record<
  string,
  Record<
    string,
    Record<string, string[]>
  >
>;

export const bangladeshLocations: LocationTree = {
  Dhaka: {
    Dhaka: {
      Dhamrai: ["Amta", "Bhararia", "Kulla"],
      Keraniganj: ["Hasnabad", "Kalatia", "Rohitpur"],
      Savar: ["Ashulia", "Birulia", "Pathalia"]
    },
    Gazipur: {
      Kaliganj: ["Baktarpur", "Jamalpur", "Tumlia"],
      Kapasia: ["Chandpur", "Durgapur", "Tokra"],
      Sreepur: ["Gazipur", "Mawna", "Telihati"]
    }
  },
  Chattogram: {
    Chattogram: {
      Anwara: ["Bairag", "Barakhain", "Raipur"],
      Patiya: ["Haidgaon", "Kusumpura", "Shikalbaha"],
      Sitakunda: ["Barabkunda", "Muradpur", "Sonaichhari"]
    },
    "Cox's Bazar": {
      Chakaria: ["Badarkhali", "Dulahazara", "Saharbil"],
      Pekua: ["Magnama", "Rajakhali", "Shilkhali"],
      Ramu: ["Fatekharkul", "Garjoniya", "Rajar Kul"]
    }
  },
  Rajshahi: {
    Bogura: {
      Dupchanchia: ["Chamayr", "Jianagar", "Talora"],
      Sherpur: ["Khanpur", "Mirzapur", "Sughatta"],
      Shibganj: ["Buriganj", "Kichak", "Majhihatta"]
    },
    Rajshahi: {
      Bagha: ["Arani", "Bausa", "Monigram"],
      Durgapur: ["Deluabari", "Gowgram", "Maria"],
      Paba: ["Damkura", "Harian", "Huzripara"]
    }
  }
};
