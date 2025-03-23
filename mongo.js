import mongoose from "mongoose";

const connectDB = () => {
  try {
    const connction = mongoose.connect(
      `mongodb+srv://nishit:seekhan@cluster0.u6w2n.mongodb.net/aushadsecondT`
    );
    console.log("COnnection succesfull")
  } catch (error) {
    console.log(`error in connecting backend ${error}`);
  }
};
export default connectDB
