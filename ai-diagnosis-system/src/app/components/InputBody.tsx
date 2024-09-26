'use client';
import { FormEvent, useCallback, useEffect, useState } from "react";

const InputBody = ({
}: {
}) => {

    async function onSubmit(event: FormEvent<HTMLFormElement>) {
        event.preventDefault()
        
        const formData = new FormData(event.currentTarget)
        const response = await fetch('/api/submit', {
            method: 'POST',
            body: formData,
        })
        
        // Handle response if necessary
        const data = await response.json()
        // ...
    }
  return (
    <div className="mt-10 mx-auto text-center">
      <h1 className="lg:text-5xl text-3xl font-bold">
        Inputs
      </h1>
      <form onSubmit={onSubmit}>
      <h1 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
        Symptoms
      </h1>
      <textarea className="caret-grey-500 border-black border-2 w-4/12"></textarea>
      <h3 className="lg:text-xl text-lg text-black-500 font-normal mt-3">
        Basic Demographic
      </h3>
      <textarea className="caret-grey-500 border-black border-2 w-4/12"></textarea>
          <br></br>
          <div className="flex items-center justify-center flex-col mt-2">
            <button type="submit" className=" py-2.5 px-4 text-center rounded-lg block font-medium text-sm text-white bg-gray-800 hover:bg-gray-600 active:bg-gray-900 md:inline">Generate</button>
          </div>
      </form>
    </div>
  );
};

export default InputBody;