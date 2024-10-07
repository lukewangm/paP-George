'use client';
import React from 'react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

// const response = await fetch('/endpoint', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({
//         symptoms,
//         demographic,
//     }),
// });

const InputBody = () => {
  const router = useRouter();
  const [result, setResult] = useState(null);

  const handleNavigation = (result: string) => {
    router.push(`/result?data=${encodeURIComponent(result)}`);
  };

  // Temporary fake response function
  const fakeFetch = () => {
    return new Promise((resolve) => {
      const list = ["link1", "link2", "link3"];
      setTimeout(() => {
        resolve({
          ok: true,
          json: async () => ({
            message: 'Fake response received!',
            data: {
              list,
            }
          }),
        });
      }, 1000); // Simulate a delay
    });
  };

  async function onSubmit(formData: { get: (arg0: string) => any; }) {
    console.log("submiting request");
    const symptoms = formData.get("symptoms");
    const lab = formData.get("lab");
    const physical = formData.get("physical");
    const age = formData.get("age");
    const sex = formData.get("sex");

    try {
      const response = await fakeFetch();
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json(); // This will call the json method
      console.log('Success:', data);
      // alert(`Response: ${JSON.stringify(data)}`); // Show the fake message
      setResult(data);
      handleNavigation(JSON.stringify(data));
    } catch (error) {
      console.error('Error:', error);
      alert('There was an error submitting your request.');
    }
  }

  return (
    <div className="mt-5 mx-auto text-center">
      <h1 className="lg:text-5xl text-3xl font-bold">
        Inputs
      </h1>
      <form action={onSubmit}>
        <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
          Symptoms
        </h1>
        <textarea name="symptoms" rows={4} className="caret-grey-500 border-black dark:border-white border-2 w-10/12 sm:w-4/12"></textarea>

        <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
          Physical exam findings
        </h1>
        <textarea name="physical" rows={4} className="caret-grey-500 border-black dark:border-white border-2 w-10/12 sm:w-4/12"></textarea>

        <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
          Abnormal lab findings
        </h1>
        <textarea name="lab" rows={4} className="caret-grey-500 border-black dark:border-white border-2 w-10/12 sm:w-4/12"></textarea>

        <h2 className=" lg:text-3xl text-3xl font-bold text-black-500 mt-3">
          Patient Details
        </h2>
        <div className="flex justify-center items-center space-x-1">
          <div >
            <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-1">
              Age
            </h1>
            <textarea name="age" rows={1} className="caret-grey-500 border-black dark:border-white border-2 w-3/12 sm:w-4/12"></textarea>
          </div>
          <div>
            <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-1">
              Sex
            </h1>
            <textarea name="sex" rows={1} className="caret-grey-500 border-black dark:border-white border-2 w-3/12 sm:w-4/12"></textarea>
          </div>
        </div>
        <br></br>
        <div className="flex items-center justify-center flex-col mt-2">
          {result ? (
            <button onClick={() => handleNavigation(result)}>Go to Result</button>
          ) : (<button type="submit" className=" py-2.5 px-4 text-center rounded-lg block font-medium text-sm text-white bg-gray-800 hover:bg-gray-600 active:bg-gray-900 md:inline">Generate</button>)}
        </div>
      </form>
    </div>
  );
};

export default InputBody;