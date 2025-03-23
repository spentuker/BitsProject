import { Medicine } from "./Medicine.js";
import connectDB from "./mongo.js";
import mongoose from "mongoose";

connectDB();
const fakeMedicines = [
  {
    medicine_name: "Paracetamol",
    created_at: new Date("2024-03-20T00:00:00.000Z"),
    dose_time: "02:33", // 3:00 PM
    validity_days: 10, // Valid for 10 days
    status: "active",
  },
  {
    medicine_name: "Aspirin",
    created_at: new Date("2024-03-18T00:00:00.000Z"),
    dose_time: "02:32", // 6:30 PM
    validity_days: 7,
    status: "active",
  },
  {
    medicine_name: "Vitamin D",
    created_at: new Date("2024-03-10T00:00:00.000Z"),
    dose_time: "02:27", // 8:00 AM
    validity_days: 14,
    status: "expired", // Since it's already expired
  },
  {
    medicine_name: "Antibiotic",
    created_at: new Date("2024-03-22T00:00:00.000Z"),
    dose_time: "02:32",
    validity_days: 5,
    status: "active",
  },
];
Medicine.insertMany(fakeMedicines)
  .then(() => {
    console.log("Fake medicine data inserted!");
    mongoose.connection.close();
  })
  .catch((err) => console.error("Error inserting data:", err));
