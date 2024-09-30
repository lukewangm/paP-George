'use client';
import { FormEvent, useCallback, useEffect, useState } from "react";

import React from 'react';
import { useRouter } from 'next/compat/router'

const InputBody = ({
}: {
}) => {

    async function onSubmit(formData: { get: (arg0: string) => any; }) {
      console.log("submiting request");
      const symptoms = formData.get("symptoms");
      const demographic = formData.get("demographic");
      const list = ["link1", "link2", "link3"];
      alert(`You searched for '${symptoms}' and ${demographic} `);

      // Temporary fake response function
      const fakeFetch = () => {
        return new Promise((resolve) => {
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

      try {

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

        const response = await fakeFetch();

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        
        const result = await response.json(); // This will call the json method
        console.log('Success:', result);
        alert(`Response: ${JSON.stringify(result)}`); // Show the fake message
        
        const router = useRouter();
        router.push({
          pathname: '/result',
          query: { data: JSON.stringify(result) }, // Pass data as a query parameter
        });

    } catch (error) {
        console.error('Error:', error);
        alert('There was an error submitting your request.');
    }
  }

  return (
    <div className="mt-10 mx-auto text-center">
      <h1 className="lg:text-5xl text-3xl font-bold">
        Inputs
      </h1>
      <form action={onSubmit}>
      <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
        Symptoms
      </h1>
      <textarea name="symptoms" rows={5} className="caret-grey-500 border-black dark:border-white border-2 w-10/12 sm:w-4/12"></textarea>
      <h3 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
        Basic Demographic
      </h3>
      <textarea name="demographic" rows={5} className="caret-grey-500 border-black dark:border-white border-2 w-10/12 sm:w-4/12"></textarea>
          <br></br>
          <div className="flex items-center justify-center flex-col mt-2">
            <button type="submit" className=" py-2.5 px-4 text-center rounded-lg block font-medium text-sm text-white bg-gray-800 hover:bg-gray-600 active:bg-gray-900 md:inline">Generate</button>
          </div>
      </form>
    </div>
  );
};

export default InputBody;