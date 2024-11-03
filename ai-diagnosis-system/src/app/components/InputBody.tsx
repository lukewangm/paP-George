'use client';
import React from 'react';
import { useRouter } from 'next/navigation';
import { useState } from 'react';

type Payload = {
  symptoms: string | null;
  lab: string | null;
  physical: string | null;
  age: string | null;
  sex: string | null;
};

interface CaseReport {
  id: string;
  title: string;
  explanation: string;
  url: string;
}

type ResponseData = [CaseReport, CaseReport, CaseReport]; // Assuming the response is an array with exactly three strings

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

async function fetchItems(payload: Payload): Promise<ResponseData> {
  try {
      const response = await fetch("http://127.0.0.1:8000/submission", {
          method: "POST",
          headers: {
              "Content-Type": "application/json"
          },
          body: JSON.stringify(payload)
      });

      if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
      }

      // real data
      var data: ResponseData = await response.json();

      //fake data for structuring
      const caseReports = [
        {
          id: "12",
          explanation: "This case is relevant because it presents a patient with pulmonary emboli that also had issues related to adrenal hemorrhage, similar to the unexpected nature of the pulmonary emboli in the current diagnosis. It highlights complications that can occur with underlying conditions that aren’t immediately apparent.",
          url: "https://jmedicalcasereports.biomedcentral.com/articles/10.1186/s13256-024-04834-3",
          title: "Bilateral adrenal hemorrhage in a postpartum woman with multiple thromboemboli: A case report"
        },
        {
          id: "16",
          explanation: "Though primarily focused on fungal infections, this case demonstrates important symptoms such as shortness of breath, which aligns with the current patient's respiratory issues. The emphasis on the diagnosis of pulmonary conditions is significant.",
          url: "https://jmedicalcasereports.biomedcentral.com/articles/10.1186/s13256-024-04836-1",
          title: "Disseminated Cryptococcus over pancreas, lung, and brain: a case report"
        },
        {
          id: "18",
          explanation: "This case deals with complications arising after a viral infection, resulting in respiratory symptoms, and although the underlying cause differs, it provides context on how respiratory issues can manifest in the post-viral stage, which may inform treatment options or considerations.",
          url: "https://jmedicalcasereports.biomedcentral.com/articles/10.1186/s13256-024-04812-9",
          title: "Circadian re-set repairs long-COVID in a prodromal Parkinson 2019s parallel: a case series"
        }
      ];
      const [item1, item2, item3] = caseReports;
      console.log("Item 1:", item1);
      console.log("Item 2:", item2);
      console.log("Item 3:", item3);
      
      // return data;
      return caseReports;

  } catch (error) {
      console.error('Error:', error);
      throw error;
  }
}

const InputBody = () => {
  const router = useRouter();
  const [result, setResult] = useState(null);

  const handleNavigation = (caseReport: CaseReport[]) => {
    const encodedData = encodeURIComponent(JSON.stringify(caseReport));
    router.push(`/result?data=${encodedData}`);
  };

  async function onSubmit(formData: { get: (arg0: string) => any; }) {
    console.log("submiting request");
    
    const payload: Payload = {
      symptoms: formData.get("symptoms"),
      lab: formData.get("lab"),
      physical: formData.get("physical"),
      age: formData.get("age"),
      sex: formData.get("sex")
  };
    try {
      const data = await fetchItems(payload)
        .then(items => {
          console.log("Received items:", items);
          handleNavigation(items);
        });
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