import mongoose from "mongoose";

const medicineSchema = new mongoose.Schema(
  {
    medicine_name: { type: String, required: true },
    created_at: { type: Date, default: Date.now }, // When the medicine entry was created
    dose_time: { type: String, required: true }, // Time format (HH:mm)
    validity_days: { type: Number, required: true }, // How many days to take the medicine
    status: {
      type: String,
      enum: ["active", "inactive", "expired"],
      default: "active",
    },
  },
  { timestamps: true }
);

// Expire medicine automatically if the validity period is over
medicineSchema.pre("save", function (next) {
  const expiryDate = new Date(this.created_at);
  expiryDate.setDate(expiryDate.getDate() + this.validity_days);
  if (new Date() >= expiryDate) {
    this.status = "expired";
  }
  next();
});

export const Medicine = mongoose.model("Medicine", medicineSchema);

