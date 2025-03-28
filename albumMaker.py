import subprocess as sp
from tkinter import filedialog, Tk


class RacoonUtilitiesInputLengthError(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


class RacoonUtilitiesMissingInputError(Exception):
	def __init__(self, message):
		self.message = message
		super().__init__(self.message)


def askExit():
	input("Press enter to exit...")
	exit()


def winDirPath(message):
	root = Tk()
	root.lift()
	root.withdraw()
	tempPath = filedialog.askdirectory(title=message, parent=root).replace('/', '\\').strip()
	return tempPath


def winFilePath(message):
	root = Tk()
	root.lift()
	root.withdraw()
	tempPath = filedialog.askopenfilename(title=message, parent=root).replace('/', '\\').strip()
	return tempPath


def winFilesPath(message):
	root = Tk()
	root.lift()
	root.withdraw()
	tempPaths = list(filedialog.askopenfilenames(title=message, parent=root))
	for i in range(len(tempPaths)):
		tempPaths[i] = tempPaths[i].replace('/', '\\')
	return tempPaths


def makeAlbum(image_input_path, sound_input_paths, final_filename, output_path):
	if image_input_path == "" or sound_input_paths == "" or final_filename == "":
		raise RacoonUtilitiesMissingInputError("No input")

	if output_path == '':
		output_path = sound_input_paths[0][:sound_input_paths[0].rfind("\\")]
	print(output_path)

	inputPath = ''
	for i in sound_input_paths:
		inputPath += f'-i "{i.replace('/', '\\')}" '

	preConcat = ''
	for i in range(0, len(sound_input_paths)):
		preConcat += f'[{i}:a]'

	extension = sound_input_paths[0][sound_input_paths[0].rfind('.'):]

	sp.run(
		f'ffmpeg {inputPath}-filter_complex "{preConcat}concat=n={len(sound_input_paths)}:v=0:a=1" {output_path}\\output{extension}',
		shell=True)
	sp.run(f'ren "{output_path}\\output{extension}" "{final_filename + extension}"', shell=True)

	sp.run(
		f'ffmpeg -r 1 -loop 1 -i "{image_input_path}" -i "{output_path}\\{final_filename + extension}" -c:v libx264 -acodec copy -r 1 -shortest -vf format=yuv420p "{output_path}\\{final_filename}.mp4"',
		shell=True)
	if f'"{output_path}\\{final_filename}.mp4"' != f'{final_filename + extension}':
		sp.run(f'del {final_filename + extension}', shell=True)



if __name__ == "__main__":
	imageInputPath = winFilePath('Pick album cover image')
	soundInputPaths = winFilesPath('Pick songs')
	finalFilename = input("Final file name: ")
	outputPath = ''
	try:
		makeAlbum(imageInputPath, soundInputPaths, finalFilename, outputPath)
	except RacoonUtilitiesMissingInputError:
		print("RacoonUtilitiesMissingInputError: No input")
		askExit()
	except RacoonUtilitiesInputLengthError:
		print("RacoonUtilitiesInputLengthError: Too many audio files selected")
		askExit()
	exit()
