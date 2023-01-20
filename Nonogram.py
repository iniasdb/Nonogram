from PIL import Image

class Monogram:
    def __init__(self, verbose):
        self._verbose = verbose
        self._rows = []
        self._cols = []

    def generate(self, width, height, image):
        self._width = width
        self._height = height
        self._image = image
        self._coords = [["_" for x in range(height)] for y in range(width)]

        self.pixelatedImg = self.convert_image()
        self.count_adjacent_col()
        self.count_adjacent_row()

    def convert_image(self) -> Image:
        # Open image
        img = Image.open(self._image)

        # Convert image to black and white
        # Dither none --> no noise
        img = img.convert('1', dither=Image.NONE)

        # Resize down to 16x16 pixels
        imgSmall = img.resize((self._width, self._height), resample=Image.Resampling.BILINEAR)
        return imgSmall

    def count_adjacent_col(self):
        # Create pixel map
        pixel_map = self.pixelatedImg.load()
        # Calc consecutive black squares/row
        cols = []

        for i in range(self._height):
            counter = 0
            col = []
            for j in range(self._width):
                if pixel_map[i,j] == 0:
                    counter+=1
                else:
                    if counter > 0:
                        col.append(counter)
                        counter = 0
            cols.append(col)
        self._cols = cols

        if self._verbose:
            # print consecutive ...
            for i in cols:
                print(i)
    
    def count_adjacent_row(self):
        # Create pixel map
        img = self.pixelatedImg.rotate(90)
        pixel_map = img.load()
        # Calc consecutive black squares/row
        rows = []

        for i in range(self._height):
            counter = 0
            row = []
            for j in range(self._width):
                if pixel_map[i,j] == 0:
                    counter+=1
                else:
                    if counter > 0:
                        row.append(counter)
                        counter = 0
            rows.append(row)
        
        self._rows = rows

        if self._verbose:
            # print consecutive ...
            for i in rows:
                print(i)

    def print_puzzle(self):
        # Find biggest list in cols
        maxCols = 0
        for col in self._cols:
            if len(col) > maxCols:
                maxCols = len(col)
        
        # Find biggest list in rows
        maxRows = 0
        for row in self._rows:
            if len(row) > maxRows:
                maxRows = len(row)

        ###
        # loop between 0 and max
        # loop cols
        # print index 0 of the biggest list first, else print " "
        # after looping cols, new line
        # print index 0 of second biggest list...
        # and so on
        # the smallest list: 0 (i == max-1), print ~
        ###
        cols = self._cols
        cols.reverse()
        first = True
        for i in range(maxCols):
            # ofset because of rows
            print("   "*maxRows, end="")

            for col in cols:
                if len(col) == maxCols-i:
                    if len(str(col[0])) == 2:
                        print(f"{col[0]}|", end="")
                    else:
                        print(f" {col[0]}|", end="")
                    col.pop(0)
                else:
                    if i == maxCols-1:
                        if first:
                            print("|", end="")
                            first = False
                        print(" ~|", end="")
                    else:
                        print("   ", end="")
            # print(" ", end="")   # TODO: backup
            print()
        
        print("---"*(len(cols)+maxRows))
        ###
        # Loop rows
        # If len() = 0 (no black squares), print " " ofset and ~
        # Else print ofset and number
        ###
        rows = self._rows
        for row in rows:
            if len(row) == 0:
                print("   "*(maxRows-1), end="")
                print(" ~", end="")
                print(" | "*(len(cols)+1), end="")
            else:
                print("   "*(maxRows-len(row)), end="")
                if len(row) > 1:
                    print(" "*(len(row)-1), end="")
                for n in row:
                    print(f" {n}", end="")
                print(" | "*(len(cols)+1), end="")
            print()
            print("---"*(len(cols)+maxRows))

    def print_image(self):
        # Create pixel map
        img = self.pixelatedImg.rotate(90)
        pixel_map = img.load()

        # Loop over pixels
        for i in range(self._height):
            for j in range(self._width):
                if pixel_map[i,j] == 0:
                    self._coords[i][j] = "x"

        # Print coordsmap
        for i in range(self._height):
            for j in range(self._width):
                print(self._coords[i][j], end="")
            print()

