import board
import busio
import adafruit_mlx90640

class ThermalCamera():

    def __init__(self) -> None:
        self.i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
        self.mlx = adafruit_mlx90640.MLX90640(self.i2c)
        self.mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

        print("MLX addr detected on I2C", [hex(i) for i in self.mlx.serial_number])

    def get(self):
        size   = (24, 32)
        mat    = [[0 for i in range(size[1])] for j in range(size[0])]
        
        buffer = [0] * (size[0] * size[1])

        while True:

            try:
                self.mlx.getFrame(buffer)
            except ValueError:
                continue

            for h in range(size[0]):
                for w in range(size[1]):
                    mat[h][w] = buffer[h*size[1]+w]

            return mat
